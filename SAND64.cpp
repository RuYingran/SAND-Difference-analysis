#include<stdio.h>
#include<stdint.h>
typedef uint32_t u32;
# define ROUNDS 48
const unsigned char SSb[16] = {
0x00 , 0x11 , 0x22 , 0xb3 , 0x44 , 0x57 , 0x66 , 0xf5 ,
0x88 , 0x99 , 0xae , 0x3d , 0xdc , 0xcf , 0x7a , 0xeb
};
u32 ROTL(u32 x, int shift) {
	return (x << shift) | (x >> (32 - shift));
}

u32 S(u32 x) {
	u32 g0 = 0, g1 = 0, t = 0;
	for (int i = 0; i < 32; i += 4) {
		t = SSb[x >> i & 0xF];
		g0 ^= (t >> 4 & 0xF) << i;
		g1 ^= (t & 0xF) << i;
	}
	return g0 ^ ROTL(g1, 4);
}

u32 G0(u32 x) {
	x ^= (x >> 3) & (x >> 2) & 0x11111111;
	x ^= (x << 3) & (x << 2) & 0x88888888;
	return x;
}
u32 G1(u32 x) {
	x ^= (x >> 1) & (x << 1) & 0x44444444;
	x ^= (x << 1) & (x >> 1) & 0x22222222;
	return x;
}
u32 P(u32 x) {
	return ROTL(x & 0x0F0F0F0F, 28) | ROTL(x & 0xF0F0F0F0,
		12);
}
void Round(const u32 Pt[], u32 Ct[], const u32 Rk[], int
	CryptRound) {
	u32 x = Pt[1], y = Pt[0],t;
	for (int r = 0; r < CryptRound; r++) {
		y ^= P(G0(x) ^ G1(ROTL(x, 4))) ^ Rk[r];
		t = x;
		x = y;
		y = t;
	}
	Ct[1] = y, Ct[0] = x;
}
void Round_S(const u32 Pt[], u32 Ct[], const u32 Rk[], int
	CryptRound) {
	u32 x = Pt[1], y = Pt[0],t;
	for (int r = 0; r < CryptRound; r++) {
		y ^= P(S(x)) ^ Rk[r];
		t = x;
		x = y;
		y = t;
	}
	Ct[1] = y, Ct[0] = x;
}

u32 A8x3(u32 x) {
	for (int i = 0; i < 3; i++) {
		x = ROTL(x, 28);
		u32 t = x >> 24 & 0xF;
		x ^= (((t << 1) | (t >> 3)) << 28) ^ ((t << 3 & 0xF)
			<< 24);
	}
	return x;
}
void KeySchedule(const u32 Mk[], u32 Rk[], int CryptRound,
	int Dec) {
	u32 t;
	Rk[3] = Mk[3], Rk[2] = Mk[2], Rk[1] = Mk[1], Rk[0] = Mk
		[0];
	for (int r = 0; r < CryptRound - 4; r++)
		Rk[r + 4] = A8x3(Rk[r + 3]) ^ Rk[r] ^ (r + 1);
	if (Dec == 1) {
		for (int r = 0; r < (int)(CryptRound / 2); r++) {
			t = Rk[r];
			Rk[r] = Rk[CryptRound - r - 1];
			Rk[CryptRound - r - 1] = t;
		}
	}
}
int main(int argc, char* argv[])
{
	u32 Pt[2] = { 0x4F5F6F7F , 0x0F1F2F3F }, Ct[2];
	u32 Mk[4] = { 0xCFDFEFFF , 0x8F9FAFBF , 0x4F5F6F7F , 0x0F1F2F3F };
	u32 Rk[ROUNDS];
	printf("Pt: 0x %08X 0x %08X\n", Pt[1], Pt[0]);
	printf("Mk: 0x %08X 0x %08X 0x %08X 0x %08X\n", Mk[3], Mk[2],
		Mk[1], Mk[0]);
	printf(" Process Enc\n");
	KeySchedule(Mk, Rk, ROUNDS, 0);
	//Round(Pt, Ct, Rk, ROUNDS);
	Round_S(Pt, Ct, Rk, ROUNDS);
	printf("Ct: 0x %08X 0x %08X\n", Ct[1], Ct[0]);
	printf(" Process Dec\n");
	KeySchedule(Mk, Rk, ROUNDS, 1);
	//Round(Ct, Pt, Rk, ROUNDS);
	Round_S(Ct, Pt, Rk, ROUNDS);
	printf("Pt: 0x %08X 0x %08X\n\n", Pt[1], Pt[0]);
	return 0;
}
