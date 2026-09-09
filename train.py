"""Train from separate, labeled train/validation folders."""
import argparse
import json
import random
import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from cnn import make_model, transform, MODEL_PATH

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data")
    parser.add_argument("--epochs", type=int, default=15)
    parser.add_argument("--batch-size", type=int, default=32)
    args = parser.parse_args()
    if args.epochs < 1 or args.batch_size < 1:
        parser.error("epochs and batch-size must be positive")
    random.seed(42)
    torch.manual_seed(42)
    train = ImageFolder(args.data + "/train", transform=transform(True))
    val = ImageFolder(args.data + "/val", transform=transform())
    expected = ["elliptical", "irregular", "spiral"]
    if train.classes != expected or train.class_to_idx != val.class_to_idx:
        raise ValueError("Both splits must contain elliptical, irregular, and spiral folders.")
    train_loader = DataLoader(train, batch_size=args.batch_size, shuffle=True)
    val_loader = DataLoader(val, batch_size=args.batch_size)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = make_model(len(train.classes)).to(device)
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
    loss_fn = nn.CrossEntropyLoss()
    best = -1
    history = []
    MODEL_PATH.parent.mkdir(exist_ok=True)
    for epoch in range(args.epochs):
        model.train()
        total_loss = 0
        for images, labels in train_loader:
            images, labels = images.to(device), labels.to(device)
            optimizer.zero_grad()
            loss = loss_fn(model(images), labels)
            loss.backward()
            optimizer.step()
            total_loss += loss.item() * len(labels)
        model.eval()
        correct = 0
        confusion = torch.zeros(3, 3, dtype=torch.int64)
        with torch.inference_mode():
            for images, labels in val_loader:
                predicted = model(images.to(device)).argmax(1).cpu()
                correct += (predicted == labels).sum().item()
                for actual, pred in zip(labels, predicted):
                    confusion[actual, pred] += 1
        accuracy = correct / len(val)
        record = {"epoch": epoch + 1, "train_loss": total_loss / len(train),
                  "validation_accuracy": accuracy, "confusion_matrix": confusion.tolist()}
        history.append(record)
        print(json.dumps(record), flush=True)
        if accuracy > best:
            best = accuracy
            torch.save({"state_dict": {k: v.cpu() for k, v in model.state_dict().items()},
                        "classes": train.classes, "validation_accuracy": accuracy}, MODEL_PATH)
    (MODEL_PATH.parent / "training_history.json").write_text(json.dumps(history, indent=2))
    print("Saved best validation checkpoint:", MODEL_PATH)

if __name__ == "__main__":
    main()
