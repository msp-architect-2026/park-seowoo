import asyncio
import httpx

URL = "http://ai.seowoo.local:32564"
VALID_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxIiwidXNlcm5hbWUiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc3MjcwNDg2OH0.0xru_052-ed-3rfz7aUoBEh0eFxab0K9cqhIxmY4kn0"

GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
RESET  = "\033[0m"
BOLD   = "\033[1m"

ATTACK_CASES = [
    {
        "name": "토큰 없이 요청",
        "cookies": {},
        "headers": {},
        "expect_blocked": True,
    },
    {
        "name": "위조 토큰 사용",
        "cookies": {"auth_token": "FAKE.INVALID.TOKEN"},
        "headers": {},
        "expect_blocked": True,
    },
    {
        "name": "alg=none 공격",
        "cookies": {"auth_token": "eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiJhZG1pbiIsInJvbGUiOiJhZG1pbiJ9."},
        "headers": {},
        "expect_blocked": True,
    },
    {
        "name": "X-Auth-User 헤더 주입",
        "cookies": {},
        "headers": {"X-Auth-User": "admin", "X-Auth-Role": "superadmin"},
        "expect_blocked": True,
    },
    {
        "name": "X-Admin 헤더 주입",
        "cookies": {},
        "headers": {"X-Admin": "true"},
        "expect_blocked": True,
    },
    {
        "name": "X-Internal-User 헤더 주입",
        "cookies": {},
        "headers": {"X-Internal-User": "root"},
        "expect_blocked": True,
    },
    {
        "name": "Authorization Bearer 위조",
        "cookies": {},
        "headers": {"Authorization": "Bearer FAKE.TOKEN.HERE"},
        "expect_blocked": True,
    },
    {
        "name": "만료된 JWT 토큰",
        "cookies": {"auth_token": "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiJ1c2VyIiwiZXhwIjoxfQ.FAKESIG"},
        "headers": {},
        "expect_blocked": True,
    },
    {
        "name": "유효한 토큰으로 정상 요청",
        "cookies": {"auth_token": VALID_TOKEN},
        "headers": {},
        "expect_blocked": False,
    },
]

async def test_auth_bypass():
    print(f"\n{BOLD}{'='*55}")
    print(f"  JWT 인증 우회 공격 방어 테스트")
    print(f"  대상: {URL}")
    print(f"{'='*55}{RESET}\n")

    passed = 0
    failed = 0
    failed_list = []

    async with httpx.AsyncClient(timeout=10, follow_redirects=False) as client:
        for case in ATTACK_CASES:
            try:
                r = await client.get(
                    URL,
                    cookies=case["cookies"],
                    headers=case["headers"]
                )
                code = r.status_code
                blocked = code in (401, 403, 302)

                if case["expect_blocked"]:
                    if blocked:
                        print(f"  {GREEN}✔{RESET} [{code}] {case['name']} → 차단됨")
                        passed += 1
                    else:
                        print(f"  {RED}✖{RESET} [{code}] {case['name']} → 차단 실패!")
                        failed += 1
                        failed_list.append(case['name'])
                else:
                    if code == 200:
                        print(f"  {GREEN}✔{RESET} [{code}] {case['name']} → 정상 통과")
                        passed += 1
                    else:
                        print(f"  {RED}✖{RESET} [{code}] {case['name']} → 정상 요청 차단됨")
                        failed += 1
                        failed_list.append(case['name'])

            except Exception as e:
                print(f"  {YELLOW}⚠{RESET} {case['name']} → 오류: {e}")
                failed += 1
                failed_list.append(case['name'])

            await asyncio.sleep(0.2)

    print(f"\n{BOLD}{'='*55}")
    print(f"  테스트 완료!")
    print(f"  통과: {GREEN}{passed}{RESET}  실패: {RED}{failed}{RESET}")
    if failed_list:
        print(f"\n  {RED}실패 항목:{RESET}")
        for f in failed_list:
            print(f"    • {f}")
    print(f"{BOLD}{'='*55}{RESET}\n")

asyncio.run(test_auth_bypass())
