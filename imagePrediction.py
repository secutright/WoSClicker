from ultralytics import YOLO

model = YOLO('res/bestV4.pt')

results = model([r'screenshots\Screenshot 2025-01-31 202817.png'], conf=.70, save=True)

boxes = results[0].boxes.xyxy.tolist()
classes = results[0].boxes.cls.tolist()
names = results[0].names
confidences = results[0].boxes.conf.tolist()

# print(boxes)
# print(classes)
# print(names)
# print(confidences)
# print(results)

for box, cls, conf in zip(boxes, classes, confidences):
    x1, y1, x2, y2 = box
    center_x = (x1+x2) / 2
    center_y = (y1+y2) / 2

    confidence = conf
    detected_class = cls
    name = names[int(cls)]

    print(f'Name: {name} Pos: {center_x}, {center_y} Conf: {confidence}')