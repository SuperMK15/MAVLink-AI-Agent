# MAVLink-AI-Agent
# 🛸 Voice-Controlled Drone Assistant with LLM + RAG

This project enables **voice-controlled operation of a drone** using an **LLM (Large Language Model)** with **Retrieval-Augmented Generation (RAG)**. Speak natural language commands like "fly 10 meters forward" or "come back to me and land" — and the system will interpret, translate, and execute them via MAVLink drone commands!

---

## ✨ Features

- 🎙️ **Speech Recognition** – Listen for user voice commands in real-time.
- 🧠 **LLM-Powered Command Parsing** – Natural language is converted into structured drone commands via Cohere API (or other LLM backends).
- 📄 **RAG-Enhanced Understanding** – Custom command documentation improves LLM accuracy and safety.
- 🚁 **Drone API Integration** – Commands are executed through a modular drone interface.
- 🔊 **Voice Feedback** – System replies verbally to confirm actions.
- ✅ **Safety & Input Validation** – Ensures proper number and type of parameters before executing.

---

## 📦 Modules

- `speech.py` – Handles speech-to-text and text-to-speech.
- `llm.py` – Interfaces with LLM APIs and sets up RAG.
- `drone.py` – Provides an abstraction over drone operations.
- `configs.py` – Loads API keys, prompt bases, command lists, and drone settings.

---

## 🧠 Example Commands

- "Take off to 5 meters"
- "Travel forward by 10 meters"
- "Yaw right by 90 degrees"
- "Go to latitude 43.651, longitude -79.383, altitude 30"
- "Return to launch"

---

## ⚙️ How It Works

1. User presses Enter to trigger listening.
2. The microphone records and converts speech to text.
3. Text is sent to an LLM along with a base prompt and command documentation.
4. The LLM returns a structured response: `<COMMAND>, <PARAM1>, <PARAM2>, ...`
5. The system parses and validates the command.
6. The command is executed via the drone interface, with spoken confirmation.

---

## 🧭 Supported Commands

| Command           | Parameters                     | Description                                 |
|------------------|--------------------------------|---------------------------------------------|
| `TAKEOFF`        | `<altitude>`                   | Arms and takes off to specified altitude    |
| `LAND`           | –                              | Lands the drone in place                    |
| `TRAVEL RELATIVE`| `<x>, <y>, <z>`                | Moves in meters relative to current pos     |
| `TRAVEL ABSOLUTE`| `<lat>, <lon>, <alt>`          | Flies to a specific GPS location            |
| `YAW RELATIVE`   | `<angle>`                      | Rotates by angle relative to heading        |
| `YAW ABSOLUTE`   | `<angle>`                      | Rotates to an absolute heading              |
| `RTL`            | –                              | Returns to launch location                  |

---

## 📁 Project Structure
```
configs/
├── commands.yaml # RAG configs for the supported commands
├── drone.yaml # configs for drone connection
├── llm.yaml # configs for the llm model
modules/
├── drone.py # Handles drone connection, arm, takeoff, land, movement, etc.
├── llm.py # Interfaces with LLM (e.g., Cohere) and supports RAG document loading
├── speech.py # Manages speech-to-text and text-to-speech functionality
├── configs.py # Loads configuration for LLM, drone, and command documentation
main.py # Entry point: listens to voice, queries LLM, commands the drone
```

---

## 🛠️ Requirements

- Python 3.7+
- Microphone and speakers
- LLM API key (Cohere)
- Recommended Python packages:
  - `speech_recognition`
  - `pyttsx3`
  - `cohere`
  - `pymavlink`
- See [requirements.txt](./requirements.txt) for more!

---

## 🚀 Getting Started

1. Clone the repo:
   ```bash
   git clone https://github.com/SuperMK15/MAVLink-AI-Agent.git
   cd MAVLink-AI-Agent
   ```

2. Create `venv` and install dependencies:
   ```bash
   python -m venv venv
   ./venv/bin/activate
   pip install -r requirements.txt
   ```

3. Set your API key for Cohere inside [llm.yaml](./configs/llm.yaml) to enable the LLM API:
   ```yaml
   api_key: "YOUR-API-KEY-HERE"
   ```

4. Start MAVLink forwarding from Mission Planner (or whatever GCS software you use) and modify the drone connection string inside [drone.yaml](./configs/drone.yaml) accordingly:
   ```yaml
   connection_string: "tcp:127.0.0.1:14550"
   ```

5. Run [main.py](./main.py):
   ```bash
   python main.py
   ```

---

## 🧪 Notes

- ⚠️ **Safety First**: Always test in a controlled environment. This system sends real-time commands to a physical drone, which may result in movement, takeoff, or landing. The maintainer of this repository takes no responsibility for damage incurred during testing, as the user is expected to always have an RC link to kill Guided mode and take manual control.
- 🧠 The LLM is configured with a base prompt and RAG documents to ensure it outputs commands in a predictable, structured format (e.g., `"COMMAND, param1, param2"`).
- 🗣️ Commands are processed through speech recognition, passed to the LLM, and parsed — make sure your voice inputs are clear and use expected phrasing.
- 🧪 Error handling is included for invalid or missing parameters, but further guardrails (e.g., geofencing, pre-checks) are encouraged.
- 💬 All recognized commands and drone responses are echoed via text-to-speech for feedback.
- 🛠️ Future improvements:
  - Improve LLM prompt tuning to minimize parsing ambiguity
  - Add state awareness (e.g., altitude, GPS lock) and report it back in natural language
  - Integrate obstacle avoidance or vision-based systems for autonomous travel commands

---

