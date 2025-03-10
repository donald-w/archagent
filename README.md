# OpenAI API Experiments

This repository contains Jupyter notebooks for experimenting with OpenAI's API and large language models.

## Setup Instructions

1. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the root directory with your OpenAI API key:
```bash
OPENAI_API_KEY=your_api_key_here
```

4. Start Jupyter Notebook:
```bash
jupyter notebook
```

5. Open `openai_examples.ipynb` to start experimenting with the OpenAI API.

## Notebook Contents

The example notebook (`openai_examples.ipynb`) includes:
- Basic chat completions
- Working with conversation history
- Different model parameters (temperature, max_tokens)
- Error handling and best practices

## Security Note
- Never commit your `.env` file to version control
- Keep your API key secure and rotate it if it's ever exposed 