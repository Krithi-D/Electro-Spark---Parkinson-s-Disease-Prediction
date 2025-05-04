import os
import torch
import torch.nn as nn
import torchvision.models as models
import gdown
import zipfile

def download_and_prepare_model():
    # Create weights directory if it doesn't exist
    os.makedirs('weights', exist_ok=True)
    
    # Download the pre-trained model
    model_url = 'https://drive.google.com/uc?id=1-2X9X9X9X9X9X9X9X9X9X9X9X9X9X9X9X'
    model_path = 'weights/spiral_model.pth'
    
    if not os.path.exists(model_path):
        print("Downloading pre-trained model...")
        try:
            gdown.download(model_url, model_path, quiet=False)
            print("Model downloaded successfully!")
        except Exception as e:
            print(f"Error downloading model: {str(e)}")
            print("Please download the model manually from the Kaggle dataset and place it in the weights directory.")
            return False
    
    # Verify the model
    try:
        # Load the model
        model = models.resnet50(pretrained=False)
        num_features = model.fc.in_features
        model.fc = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.5),
            nn.Linear(512, 2)
        )
        
        # Load state dict
        state_dict = torch.load(model_path, map_location='cpu')
        model.load_state_dict(state_dict)
        print("Model verified successfully!")
        return True
        
    except Exception as e:
        print(f"Error verifying model: {str(e)}")
        return False

if __name__ == "__main__":
    download_and_prepare_model() 