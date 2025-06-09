#define ORANGE    21 // 29
#define YELLOW    22 // 31
#define PINK      23 // 33
#define BLUE      24 // 35
#define RED       25 // 임시 전원용 : 사용 불가
// GND        6
// 5V         2

void step_wave(int step);
void step_full(int step); // 4phase 4setp full
void step_half(int step); // 4phase 8step full
