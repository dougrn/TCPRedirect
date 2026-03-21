# 🚀 TCPRedirect

**TCPRedirect** is a powerful and lightweight TCP proxy written in Python using `asyncio`. It allows you to redirect traffic from one or more local ports to any other specified host and port.

This tool is specifically designed to bypass local-only service restrictions by proxying external connections through a local instance, making them appear as `localhost` to the target service.

---

## 🌟 Features

-   **Multi-Port Support**: Redirect multiple ports simultaneously using a single instance.
-   **Async Performance**: Built on top of Python's `asyncio` for high concurrency and low overhead.
-   **Simple Configuration**: Easy-to-manage `config.json` for all your mapping needs.
-   **Professional Logging**: Clean, timestamped logs to monitor your data flow in real-time.
-   **Graceful Shutdown**: Properly handles termination signals to ensure all connections are closed safely.

---

## 📂 Project Structure

```text
TCPRedirect/
├── config.json         # Port mappings configuration
├── redirector.py       # Core proxy logic
├── .gitignore          # Git ignore rules
└── README.md           # Documentation
```

---

## 🛠️ Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dougrn/TCPRedirect.git
    cd TCPRedirect
    ```

2.  **Ensure you have Python 3.7+ installed.**

3.  **No external dependencies required!** (Uses Python Standard Library).

---

## 🚀 Usage

### 1. Configure Mappings
Edit `config.json` to define your port redirects. Each mapping consists of:
-   `listen_port`: The port TCPRedirect will listen on.
-   `target_host`: The destination host (e.g., `127.0.0.1`).
-   `target_port`: The destination port.

```json
{
  "mappings": [
    {
      "comment": "Redirect external 8091 to local 8090",
      "listen_port": 8091,
      "target_host": "127.0.0.1",
      "target_port": 8090
    }
  ]
}
```

### 2. Run the Redirector
```bash
python redirector.py
```

---

## 💡 How it works

When TCPRedirect receives a connection on a `listen_port`, it establishes a new connection to the `target_host:target_port`. It then creates a bidirectional bridge, forwarding all data between the original client and the target service.

Since TCPRedirect typically runs on the same machine as the target service, the service sees the connection coming from `127.0.0.1`, effectively bypassing IP-based access restrictions.

---

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Developed with ❤️ by [dougrn](https://github.com/dougrn)
