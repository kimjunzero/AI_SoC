import cv2
import sys
import threading
import time
import torch

# ─────────────────────────────────────────────────────────────────────────────
# 1) YOLOv5 모델 로드 및 설정
#    - ultralytics/yolov5s 사전학습 모델을 불러옵니다.
#    - COCO 데이터셋에서 'car', 'truck', 'bus', 'motorcycle' 클래스만 필터링합니다.
#    - DETECT_INTERVAL은 YOLO 추론 주기(초 단위)입니다.
#
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
CONF_THRESH = 0.4
DETECT_INTERVAL = 0.2  # YOLO 추론 주기(초)

# COCO 데이터셋에서 차량 관련 클래스 인덱스
#   'car' = 2, 'motorcycle' = 3, 'bus' = 5, 'truck' = 7
VEHICLE_CLASSES = [2, 3, 5, 7]

# ─────────────────────────────────────────────────────────────────────────────
# 2) 전역 변수 선언
#    - latest_frame_i: i번째 카메라에서 마지막으로 읽은 프레임
#    - latest_boxes_i: i번째 카메라에 대한 YOLO 검출 결과(바운딩박스 리스트)
#
latest_frame_0 = None
latest_frame_1 = None

latest_boxes_0 = []  # [(xmin, ymin, xmax, ymax, label), ...]
latest_boxes_1 = []

# 캡처 인덱스 (환경에 따라 /dev/video0=0, /dev/video1=1 또는 /dev/video2 등으로 바꿔 주세요)
CAM_IDX_LEFT  = 0
CAM_IDX_RIGHT = 2

# 각 카메라의 해상도 (원하는 크기로 설정)
DESIRED_WIDTH  = 480
DESIRED_HEIGHT = 360

# ─────────────────────────────────────────────────────────────────────────────
# 3) YOLO 추론을 별도 스레드에서 수행하는 함수 정의
#    - detect_loop_0(): 첫 번째 카메라 프레임을 주기적으로 가져와서 YOLO로 검출
#    - detect_loop_1(): 두 번째 카메라 프레임을 주기적으로 가져와서 YOLO로 검출
#
def detect_loop_0():
    global latest_frame_0, latest_boxes_0
    while True:
        if latest_frame_0 is None:
            time.sleep(0.01)
            continue

        # 프레임 복사 (메인 루프에서 overwrite 방지)
        frame = latest_frame_0.copy()
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # YOLOv5 추론
        results = model(img_rgb)
        df = results.pandas().xyxy[0]
        # 차량 클래스만 필터링
        vehicle_df = df[
            (df['name'].isin(['car', 'truck', 'bus', 'motorcycle'])) &
            (df['confidence'] > CONF_THRESH)
        ]

        boxes = []
        for _, row in vehicle_df.iterrows():
            xmin = int(row['xmin'])
            ymin = int(row['ymin'])
            xmax = int(row['xmax'])
            ymax = int(row['ymax'])
            label = f"{row['name']} {row['confidence']:.2f}"
            boxes.append((xmin, ymin, xmax, ymax, label))

        latest_boxes_0 = boxes
        time.sleep(DETECT_INTERVAL)


def detect_loop_1():
    global latest_frame_1, latest_boxes_1
    while True:
        if latest_frame_1 is None:
            time.sleep(0.01)
            continue

        # 프레임 복사 (메인 루프에서 overwrite 방지)
        frame = latest_frame_1.copy()
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # YOLOv5 추론
        results = model(img_rgb)
        df = results.pandas().xyxy[0]
        # 차량 클래스만 필터링
        vehicle_df = df[
            (df['name'].isin(['car', 'truck', 'bus', 'motorcycle'])) &
            (df['confidence'] > CONF_THRESH)
        ]

        boxes = []
        for _, row in vehicle_df.iterrows():
            xmin = int(row['xmin'])
            ymin = int(row['ymin'])
            xmax = int(row['xmax'])
            ymax = int(row['ymax'])
            label = f"{row['name']} {row['confidence']:.2f}"
            boxes.append((xmin, ymin, xmax, ymax, label))

        latest_boxes_1 = boxes
        time.sleep(DETECT_INTERVAL)


# ─────────────────────────────────────────────────────────────────────────────
# 4) 메인 함수: 두 카메라 열기, 스레드 시작, 프레임 읽기 & 시각화
#
def main():
    global latest_frame_0, latest_frame_1

    # 4-1) 첫 번째, 두 번째 카메라 VideoCapture 생성 (V4L2 백엔드 강제)
    cap0 = cv2.VideoCapture(CAM_IDX_LEFT,  cv2.CAP_V4L2)
    cap1 = cv2.VideoCapture(CAM_IDX_RIGHT, cv2.CAP_V4L2)

    # 해상도 설정
    cap0.set(cv2.CAP_PROP_FRAME_WIDTH,  DESIRED_WIDTH)
    cap0.set(cv2.CAP_PROP_FRAME_HEIGHT, DESIRED_HEIGHT)
    cap1.set(cv2.CAP_PROP_FRAME_WIDTH,  DESIRED_WIDTH)
    cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, DESIRED_HEIGHT)

    # 4-2) 카메라 열기 실패 시 에러 처리
    if not cap0.isOpened():
        print(f"Error: 첫 번째 카메라(index={CAM_IDX_LEFT}) 열기 실패")
        cap0.release()
        cap1.release()
        cv2.destroyAllWindows()
        sys.exit(1)
    else:
        print(f"첫 번째 카메라(index={CAM_IDX_LEFT}) 정상 열림 → 해상도: {DESIRED_WIDTH}×{DESIRED_HEIGHT}")

    if not cap1.isOpened():
        print(f"Error: 두 번째 카메라(index={CAM_IDX_RIGHT}) 열기 실패")
        cap0.release()
        cap1.release()
        cv2.destroyAllWindows()
        sys.exit(1)
    else:
        print(f"두 번째 카메라(index={CAM_IDX_RIGHT}) 정상 열림 → 해상도: {DESIRED_WIDTH}×{DESIRED_HEIGHT}")

    # 4-3) YOLO 추론 스레드 두 개 시작
    threading.Thread(target=detect_loop_0, daemon=True).start()
    threading.Thread(target=detect_loop_1, daemon=True).start()

    # 4-4) 윈도우 생성 (두 영상 나란히 보려면 하나의 창으로 가로 병합해서 출력)
    window_name = "Cam 0 (Left) | Cam 2 (Right) - YOLOv5 Vehicle Detection"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    # 4-5) 메인 루프: 두 카메라 프레임 읽기 → 글로벌에 저장 → YOLO 결과 오버레이 → 화면 출력
    while True:
        # 첫 번째(N=0) 카메라 프레임 읽기
        ret0, frame0 = cap0.read()
        if not ret0:
            print("Warning: 첫 번째 카메라 프레임 읽기 실패")
        else:
            latest_frame_0 = frame0.copy()  # YOLO 스레드가 읽을 수 있도록 전역 변수에 저장

        # 두 번째(N=1) 카메라 프레임 읽기
        ret1, frame1 = cap1.read()
        if not ret1:
            print("Warning: 두 번째 카메라 프레임 읽기 실패")
        else:
            latest_frame_1 = frame1.copy()

        # 4-6) 검출된 바운딩박스 가져와서 오버레이
        # 첫 번째 카메라
        if ret0 and latest_boxes_0:
            for xmin, ymin, xmax, ymax, label in latest_boxes_0:
                cv2.rectangle(frame0, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(frame0, label, (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 두 번째 카메라
        if ret1 and latest_boxes_1:
            for xmin, ymin, xmax, ymax, label in latest_boxes_1:
                cv2.rectangle(frame1, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                cv2.putText(frame1, label, (xmin, ymin - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # 4-7) 화면에 두 영상을 가로로 이어 붙여서 표시
        if ret0 and ret1:
            combined = cv2.hconcat([frame0, frame1])
        elif ret0:
            combined = frame0
        elif ret1:
            combined = frame1
        else:
            combined = None  # 둘 다 실패 시 None

        if combined is not None:
            cv2.imshow(window_name, combined)

        # 4-8) ESC 키 누르면 종료
        if cv2.waitKey(1) & 0xFF == 27:
            print("ESC 입력: 프로그램 종료")
            break

    # 4-9) 자원 해제
    cap0.release()
    cap1.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
