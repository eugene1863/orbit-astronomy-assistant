"""Shared CNN architecture and inference. Imports are optional for text chat."""
from pathlib import Path
import torch
from torch import nn
from torchvision import transforms
from PIL import Image
MODEL_PATH = Path(__file__).parent / "models" / "galaxy_cnn.pt"
IMAGE_SIZE = 128

def make_model(classes=3):
    return nn.Sequential(
        nn.Conv2d(3, 16, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(16, 32, 3, padding=1), nn.ReLU(), nn.MaxPool2d(2),
        nn.Conv2d(32, 64, 3, padding=1), nn.ReLU(),
        nn.AdaptiveAvgPool2d((4, 4)), nn.Flatten(),
        nn.Linear(64 * 4 * 4, 128), nn.ReLU(), nn.Dropout(0.3),
        nn.Linear(128, classes))

def transform(training=False):
    ops = [transforms.Resize((IMAGE_SIZE, IMAGE_SIZE))]
    if training:
        ops += [transforms.RandomHorizontalFlip(), transforms.RandomVerticalFlip(),
                transforms.RandomRotation(180)]
    return transforms.Compose(ops + [transforms.ToTensor(),
        transforms.Normalize([0.5]*3, [0.5]*3)])

def classify(stream):
    checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=True)
    classes = checkpoint["classes"]
    model = make_model(len(classes))
    model.load_state_dict(checkpoint["state_dict"])
    model.eval()
    with Image.open(stream) as image:
        image.load()
        tensor = transform()(image.convert("RGB")).unsqueeze(0)
    with torch.inference_mode():
        scores = model(tensor).softmax(dim=1)[0].tolist()
    return {"label": classes[max(range(len(scores)), key=scores.__getitem__)],
            "scores": dict(zip(classes, scores)),
            "note": "These are uncalibrated model scores, not verified probabilities. Use a cropped galaxy image; this model cannot detect unrelated images reliably."}
