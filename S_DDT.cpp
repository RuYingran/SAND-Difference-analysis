#include <stdio.h>
#include <stdint.h>

typedef uint32_t u32;
typedef uint8_t u8;
//DDT 计算差分分布表
const unsigned char SSb[16] = {
0x00 , 0x11 , 0x22 , 0xb3 , 0x44 , 0x57 , 0x66 , 0xf5 ,
0x88 , 0x99 , 0xae , 0x3d , 0xdc , 0xcf , 0x7a , 0xeb
};
int S(int x) {
	return SSb[x];
}
int main() {
	int a=0xF, x;
	int b=0x69;
	int count = 0;
	int matrix[16][256] = { 0 };
	for (a=0x0; a <= 0xF; a++) {
		for (b=0x0; b <= 0xFF; b++) {
			for (x = 0x0; x <= 0xF; x++) {
				if ((S(x) ^ S(x ^ a)) == b) {
					matrix[a][b] += 1;
				}
			}
		}
	}
	for (int i = 0; i < 16; i++) {
		printf("\n");
		for (int j = 0; j < 256; j++) {
			//printf("%d",matrix[i][j]);
			if (matrix[i][j] != 0) {
				printf("0x%x",i);
				printf("\t");
				printf("%d", matrix[i][j]);
				printf("\t");
				printf("0x%x", j);
				printf("\n");
			}
		}
	}
	
}

