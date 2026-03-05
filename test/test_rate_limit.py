import asyncio
import httpx
import time

URL = "http://ai.seowoo.local:32564"
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc3MjcwNDg2OH0.0xru_052-ed-3rfz7aUoBEh0eFxab0K9cqhIxmY4kn0"
COOKIES = {"auth_token": TOKEN}

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

async def test_rate_limit():
    print(f"\n{BOLD}{'='*55}")
    print(f"  Rate Limiting 검증 테스트")
    print(f"  대상: {URL}")
    print(f"{'='*55}{RESET}\n")

    async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:

        # ── 테스트 1: 정상 요청 ──────────────────────────────
        print(f"{BOLD}[테스트 1] 정상 범위 요청 (8개, 1초당){RESET}")
        ok_count = 0
        for i in range(8):
            r = await client.get(URL, cookies=COOKIES)
            status = r.status_code
            mark = f"{GREEN}✔{RESET}" if status != 429 else f"{RED}✖{RESET}"
            print(f"  {mark} 요청 {i+1}: HTTP {status}")
            if status != 429:
                ok_count += 1
            await asyncio.sleep(0.13)

        result = f"{GREEN}통과{RESET}" if ok_count == 8 else f"{RED}실패{RESET}"
        print(f"  결과: {ok_count}/8 정상 응답 → {result}\n")

        # ── 테스트 2: 버스트 요청 → 429 확인 ────────────────
        print(f"{BOLD}[테스트 2] 버스트 요청 30개 동시 전송{RESET}")
        tasks = [client.get(URL, cookies=COOKIES) for _ in range(30)]
        start = time.perf_counter()
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        elapsed = time.perf_counter() - start

        s200 = sum(1 for r in responses if not isinstance(r, Exception) and r.status_code == 200)
        s429 = sum(1 for r in responses if not isinstance(r, Exception) and r.status_code in (429, 503))
        err  = sum(1 for r in responses if isinstance(r, Exception))

        print(f"  {GREEN}✔{RESET} HTTP 200: {s200}개")
        print(f"  {RED}✖{RESET} HTTP 429: {s429}개 (Rate Limited)")
        if err:
            print(f"  {YELLOW}⚠{RESET} 오류: {err}개")
        print(f"  소요시간: {elapsed:.2f}초")
        result = f"{GREEN}통과{RESET}" if s429 > 0 else f"{RED}실패 - 429 없음{RESET}"
        print(f"  결과: Rate Limit 발동 → {result}\n")

        # ── 테스트 3: 회복 확인 ───────────────────────────────
        print(f"{BOLD}[테스트 3] Rate Limit 회복 (2초 대기 후){RESET}")
        await asyncio.sleep(2)
        r = await client.get(URL, cookies=COOKIES)
        mark = f"{GREEN}✔{RESET}" if r.status_code != 429 else f"{RED}✖{RESET}"
        result = f"{GREEN}통과{RESET}" if r.status_code != 429 else f"{RED}실패{RESET}"
        print(f"  {mark} 회복 후 상태: HTTP {r.status_code} → {result}\n")

        # ── 최종 요약 ─────────────────────────────────────────
        print(f"{BOLD}{'='*55}")
        print(f"  테스트 완료!")
        print(f"  정상요청 허용: {'✔' if ok_count==8 else '✖'}")
        print(f"  버스트 차단:   {'✔' if s429>0 else '✖'}")
        print(f"  회복 확인:     {'✔' if r.status_code!=429 else '✖'}")
        print(f"{'='*55}{RESET}\n")

asyncio.run(test_rate_limit())
