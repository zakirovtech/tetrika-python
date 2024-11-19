import unittest
from unittest.mock import patch, MagicMock
import httpx
from task2.solution import gather_names


class TestGatherNames(unittest.TestCase):
    @patch("task2.config.settings")
    def test_gather_names_success(self, mock_settings):
        mock_settings.headers = {"User-Agent": "test-agent"}
        mock_settings.domain = "https://example.com"
        mock_settings.rus_chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        
        # Mocked HTML
        html_page_1 = """
        <html>
            <div class="mw-category mw-category-columns">
                <ul>
                    <li>Антилопа</li>
                    <li>Бобр</li>
                </ul>
            </div>
            <a href="/next_page">Следующая страница</a>
        </html>
        """
        html_page_2 = """
        <html>
            <div class="mw-category mw-category-columns">
                <ul>
                    <li>Волк</li>
                    <li>Гепард</li>
                </ul>
            </div>
            <a href="/final_page">Следующая страница</a>
        </html>
        """
        html_page_final = """
        <html>
            <div class="mw-category mw-category-columns">
                <ul>
                    <li>Дятел</li>
                    <li>Zebra</li>
                </ul>
            </div>
            <a href='#'>Следующая страница</a>
        </html>
        """
        
        mock_responses = [
            MagicMock(status_code=200, text=html_page_1),
            MagicMock(status_code=200, text=html_page_2),
            MagicMock(status_code=200, text=html_page_final),
        ]

        def mock_get(url, headers):
            return mock_responses.pop(0)

        # Mocked httpx.Client
        with patch.object(httpx.Client, "get", side_effect=mock_get):
            session = httpx.Client()

            gather_names(session=session, url="https://example.com/start")

    @patch("task2.config.settings")
    def test_gather_names_no_next_page(self, mock_settings):
        mock_settings.headers = {"User-Agent": "test-agent"}
        mock_settings.domain = "https://example.com"
        mock_settings.rus_chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        
        html_page = """
        <html>
            <div class="mw-category mw-category-columns">
                <ul>
                    <li>Антилопа</li>
                    <li>Бобр</li>
                </ul>
            </div>
        </html>
        """

        mock_response = MagicMock(status_code=200, text=html_page)

        with patch.object(httpx.Client, "get", return_value=mock_response):
            session = httpx.Client()

            gather_names(session=session, url="https://example.com/start")

    @patch("task2.config.settings")
    @patch("task2.solution.make_backup")
    def test_gather_names_error_handling(self, mock_make_backup, mock_settings):
        mock_settings.headers = {"User-Agent": "test-agent"}
        mock_settings.domain = "https://example.com"
        mock_settings.rus_chars = "абвгдеёжзийклмнопрстуфхцчшщъыьэюя"
        
        mock_response = MagicMock(status_code=500)

        with patch.object(httpx.Client, "get", return_value=mock_response):
            session = httpx.Client()

            with self.assertLogs("streamLogger", level="ERROR") as log:
                gather_names(session=session, url="https://example.com/start")
            
            self.assertIn("Failed load the source page", log.output[0])

        mock_make_backup.assert_called_once()
        self.assertEqual(mock_make_backup.call_args[0][0], {"https://example.com/start": []})
