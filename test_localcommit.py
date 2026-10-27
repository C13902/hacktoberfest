import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, HTTPServer

from localcommit.llm import LLMError, chat
from localcommit.prompt import build_messages, clean_message


class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        self.rfile.read(int(self.headers["Content-Length"]))
        body = json.dumps({"choices": [{"message": {"content": "feat: add thing"}}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *a):
        pass


class Tests(unittest.TestCase):
    def test_clean_fences_and_quotes(self):
        self.assertEqual(clean_message("```\nfix: x\n```"), "fix: x")
        self.assertEqual(clean_message('"fix: x"'), "fix: x")

    def test_truncation(self):
        m = build_messages("a" * 100, max_chars=10)
        self.assertIn("[diff truncated]", m[1]["content"])

    def test_bad_style(self):
        with self.assertRaises(ValueError):
            build_messages("x", style="nope")

    def test_chat_against_mock_server(self):
        srv = HTTPServer(("127.0.0.1", 0), Handler)
        threading.Thread(target=srv.serve_forever, daemon=True).start()
        out = chat(f"http://127.0.0.1:{srv.server_port}/v1", "m", [{"role": "user", "content": "hi"}])
        srv.shutdown()
        self.assertEqual(out, "feat: add thing")

    def test_unreachable(self):
        with self.assertRaises(LLMError):
            chat("http://127.0.0.1:1/v1", "m", [], timeout=2)


if __name__ == "__main__":
    unittest.main()
