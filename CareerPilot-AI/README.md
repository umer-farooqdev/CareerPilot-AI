# CareerPilot AI — Student Career Guidance

CareerPilot AI is a beginner-friendly web app prototype for exploring career paths. A student enters their education, interests, current skills, and goal. The app returns three career ideas, suggested skills, portfolio project ideas, and a four-week learning roadmap.

Built as an MVP for the Pak Angels Final Hackathon (October 2026).

## Features

- Responsive homepage and student profile form
- Gemini AI career suggestions when `GEMINI_API_KEY` is configured
- Built-in demo recommendations when no API key is available or the AI request fails
- Career relevance indicator (not a probability or validated aptitude score)
- Skills to develop, project ideas, and a four-week roadmap
- Print / Save as PDF report
- No database or account system in this MVP

## Tech stack

- Python 3.10+
- Flask
- Google Gen AI Python SDK
- HTML and CSS
- python-dotenv

## Run in VS Code (Windows)

1. Install Python 3.10 or newer from https://www.python.org/downloads/ . During installation, select **Add Python to PATH**.
2. Download or clone this repository and open the `CareerPilot-AI` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

   ```powershell
   py -m venv .venv
   ```

5. Activate it in PowerShell:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt in VS Code and run:

   ```cmd
   .venv\Scripts\activate.bat
   ```

6. Install packages:

   ```powershell
   python -m pip install -r requirements.txt
   ```

7. Optional: enable Gemini AI. Copy `.env.example` to a new file named `.env`, then replace the placeholder with your own Gemini API key:

   ```text
   GEMINI_API_KEY=your_actual_key_here
   ```

   Create/manage a key at https://aistudio.google.com/apikey . Do not share the key or upload `.env` to GitHub. The `.gitignore` file excludes it.

8. Start the app:

   ```powershell
   python app.py
   ```

9. Open http://127.0.0.1:5000 in your browser.
10. Fill in the form and select **Generate my career roadmap**. If no key is configured, the demo recommendation engine still works.

## Common issues

- **`python` or `py` not recognized:** reinstall Python and enable Add Python to PATH, then restart VS Code.
- **`No module named flask`:** activate `.venv` and run `python -m pip install -r requirements.txt`.
- **Gemini returns an error:** check that the key is valid, billing/usage access and quotas are available for your account, and the model is available. The app falls back to demo suggestions.
- **PowerShell activation blocked:** use the Command Prompt activation command shown above. You can also run `.venv\Scripts\python.exe app.py` without activating.
- **Port 5000 already in use:** close the other app using it or change the final line in `app.py` to `app.run(debug=True, port=5001)` and visit `http://127.0.0.1:5001`.

## Project structure

```text
CareerPilot-AI/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── templates/
│   ├── index.html
│   └── results.html
└── static/
    └── style.css
```

## Responsible use

Career suggestions are exploratory and may be incomplete or inaccurate. The match indicator is an approximate relevance indicator, not a probability of success, psychometric score, or guarantee of employment. Students should research careers and consult teachers, mentors, and professionals before making major decisions. Do not enter sensitive personal information.

## Suggested next improvements

- Save reports locally or add optional accounts
- Add a user-editable progress tracker
- Add verified course links and local internship resources
- Add automated tests and accessibility review
- Deploy with environment variables configured securely

## Hackathon demo script (60–90 seconds)

1. Introduce the problem: students need a practical starting point for career exploration.
2. Open the form and enter a sample profile (no private details).
3. Generate the three career paths.
4. Explain the suggested skills, project ideas, and four-week roadmap.
5. Print the report to PDF.
6. Explain that Gemini powers personalized suggestions when configured, while demo mode ensures the prototype remains usable without a key.

## License

For hackathon/educational demonstration. Add a license if you choose to publish the project for broader reuse.
