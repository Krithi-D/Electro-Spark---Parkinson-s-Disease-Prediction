# Electro Spark - Early Parkinson's Disease Detection

Electro Spark is an AI-powered web application for early detection of Parkinson's disease using voice analysis and spiral drawing analysis.

## Features
- Voice sample analysis using Wav2Vec2.0
- Spiral drawing analysis using ResNet-50
- Web-based interface using Streamlit
- Non-invasive and accessible screening
- Remote screening capabilities

## Project Structure
```
electro_spark/
├── models/
│   ├── voice_model.py
│   └── spiral_model.py
├── utils/
│   ├── audio_processor.py
│   └── image_processor.py
├── app.py
├── requirements.txt
└── README.md
```

## Setup Instructions
1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run app.py
```

## Model Training
- Voice model: Uses Wav2Vec2.0 for feature extraction
- Spiral model: Uses ResNet-50 for image classification

## Data Collection
- Voice samples: Recorded audio files (.wav format)
- Spiral drawings: Digital images of hand-drawn spirals

## Contributing
Please read CONTRIBUTING.md for details on our code of conduct and the process for submitting pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details. 