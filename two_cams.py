# two_cams.py

import cv2
import sys

def main():
    # ──────────────────────────────────────────────────────────
    # 1) 웹캠 인덱스와 원하는 해상도 설정
    #
    #    - 왼쪽 카메라: /dev/video0 → index=0
    #    - 오른쪽 카메라: /dev/video1 → index=2
    #
    cam_idx_left  = 0
    cam_idx_right = 2

    # 원하는 해상도 (가로 × 세로)
    DESIRED_WIDTH  = 480
    DESIRED_HEIGHT = 360

    # ──────────────────────────────────────────────────────────
    # 2) VideoCapture 객체 생성 (V4L2 백엔드 강제 사용)
    #
    #    Linux/라즈베리파이의 경우, 기본적으로 GStreamer 파이프라인을 쓰는데
    #    제대로 설치되어 있지 않으면 열리지 않는 경우가 많습니다.
    #    cv2.CAP_V4L2 플래그를 주면 v4l2 드라이버를 바로 불러와 줍니다.
    cap_left  = cv2.VideoCapture(cam_idx_left,  cv2.CAP_V4L2)
    cap_right = cv2.VideoCapture(cam_idx_right, cv2.CAP_V4L2)

    # ──────────────────────────────────────────────────────────
    # 3) 해상도 설정 (카메라가 실제 지원하는 해상도로만 설정해야 함)
    #
    #    지원하지 않는 해상도를 set() 하면 파이프라인 생성에 실패하여
    #    cap.isOpened()가 False가 될 수 있습니다.
    cap_left .set(cv2.CAP_PROP_FRAME_WIDTH,  DESIRED_WIDTH)
    cap_left .set(cv2.CAP_PROP_FRAME_HEIGHT, DESIRED_HEIGHT)
    cap_right.set(cv2.CAP_PROP_FRAME_WIDTH,  DESIRED_WIDTH)
    cap_right.set(cv2.CAP_PROP_FRAME_HEIGHT, DESIRED_HEIGHT)

    # ──────────────────────────────────────────────────────────
    # 4) 카메라 정상 연결 여부 검사
    if not cap_left.isOpened():
        print(f"Error: 왼쪽 카메라(index={cam_idx_left})를 열 수 없습니다.")
        cap_left.release()
        cap_right.release()
        cv2.destroyAllWindows()
        sys.exit(1)
    else:
        print(f"왼쪽 카메라(index={cam_idx_left}) 정상 열림  →  해상도 {DESIRED_WIDTH}×{DESIRED_HEIGHT}")

    if not cap_right.isOpened():
        print(f"Error: 오른쪽 카메라(index={cam_idx_right})를 열 수 없습니다.")
        cap_left.release()
        cap_right.release()
        cv2.destroyAllWindows()
        sys.exit(1)
    else:
        print(f"오른쪽 카메라(index={cam_idx_right}) 정상 열림  →  해상도 {DESIRED_WIDTH}×{DESIRED_HEIGHT}")

    # ──────────────────────────────────────────────────────────
    # 5) 메인 루프: 두 카메라 동시에 읽어서 한 화면에 가로로 나란히 붙여서 보여주기
    window_name = "Cam 0 (Left) | Cam 2 (Right)"
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)

    while True:
        ret_l, frame_l = cap_left.read()
        ret_r, frame_r = cap_right.read()

        # 하나라도 프레임 읽기 실패하면 경고 출력
        if not ret_l:
            print("Warning: 왼쪽 카메라에서 프레임을 읽지 못했습니다.")
        if not ret_r:
            print("Warning: 오른쪽 카메라에서 프레임을 읽지 못했습니다.")

        if ret_l and ret_r:
            # 두 프레임이 정상적으로 읽혔으면, 가로로 붙여서 화면에 띄우기
            combined = cv2.hconcat([frame_l, frame_r])
            cv2.imshow(window_name, combined)
        else:
            # 어느 한쪽이라도 읽기 실패 시, 검은 화면(black)으로 대체
            # (가로×세로 1채널 검은 이미지를 만든 뒤, 3채널 BGR로 변환)
            blank_gray = 0 * (frame_l if ret_l else frame_r)
            blank_bgr  = cv2.cvtColor(blank_gray, cv2.COLOR_GRAY2BGR)

            left_disp  = frame_l if ret_l else blank_bgr
            right_disp = frame_r if ret_r else blank_bgr
            combined   = cv2.hconcat([left_disp, right_disp])
            cv2.imshow(window_name, combined)

        # ESC 키(키값 27) 누르면 루프 탈출 → 종료
        if cv2.waitKey(1) & 0xFF == 27:
            print("ESC 입력 → 프로그램 종료")
            break

    # ──────────────────────────────────────────────────────────
    # 6) 자원 해제
    cap_left.release()
    cap_right.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
