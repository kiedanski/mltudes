# %%
import cv2
import matplotlib.pyplot as plt
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
from tqdm import tqdm
from transformers import CLIPSegForImageSegmentation, CLIPSegProcessor

# %%


def build_preprocess(smaller_dimension):
    return transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.CenterCrop(smaller_dimension),
            transforms.Resize(352),
            transforms.ToPILImage(),
        ]
    )


# %%
processor = CLIPSegProcessor.from_pretrained("CIDAS/clipseg-rd64-refined")
model = CLIPSegForImageSegmentation.from_pretrained("CIDAS/clipseg-rd64-refined")

# %%


def load_video_as_frames(filename):
    video = cv2.VideoCapture(filename)
    frames = []
    preprocess = None
    i = 0
    while True:
        ret, frame = video.read()
        if not ret:
            break
        if i == 0:
            dim = min(frame.shape[0], frame.shape[1])
            preprocess = build_preprocess(dim)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = preprocess(Image.fromarray(frame))
        frames.append(image)
        i += 1

    video.release()
    return frames


# %%
walking_frames = load_video_as_frames("walking.mp4")

# %%
background_frames = load_video_as_frames("background.mp4")


# %%
def open_image(path):
    image = Image.open(path)
    smaller_dim = min(image.height, image.width)

    preprocess = transforms.Compose(
        [
            transforms.ToTensor(),
            transforms.CenterCrop(smaller_dim),
            transforms.Resize(352),
            transforms.ToPILImage(),
        ]
    )

    cropped_image = preprocess(image)
    return cropped_image


# %%
N = min(len(walking_frames), len(background_frames))
SEGMENT_NAME = "tshirt"
THRESHOLD = 0.3
# %%
final_frame = []
for i, f in enumerate(tqdm(walking_frames[:N])):
    inputs = processor(
        text=SEGMENT_NAME, images=f, padding="max_length", return_tensors="pt"
    )
    # predict
    with torch.no_grad():
        outputs = model(**inputs)
    mask = torch.sigmoid(outputs.logits)
    mixed_image = transforms.ToPILImage()(
        transforms.ToTensor()(f) * (mask <= THRESHOLD).unsqueeze(0)
        + transforms.ToTensor()(background_frames[i]) * (mask > THRESHOLD).unsqueeze(0)
    )
    final_frame.append(mixed_image)
# %%

fourcc = cv2.VideoWriter_fourcc(*"mp4v")
out = cv2.VideoWriter("output.mp4", fourcc, 30.0, (352, 352))
for f in final_frame:
    opencv_image = cv2.cvtColor(np.array(f), cv2.COLOR_RGB2BGR)
    out.write(opencv_image)
out.release()


# %%
