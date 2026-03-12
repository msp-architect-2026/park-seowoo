# 🛡️ K8S 기반 보안 API 게이트웨이 시스템
> **Kubernetes 기반의 Zero-Trust 보안 아키텍처로 Groq Cloud AI API를 안전하게 중계·제어하는 클라우드 네이티브 인프라**

---

## 📌 프로젝트 개요

AI 서비스 확산에 따른 **DDoS, API Key 노출, 무분별한 API 호출** 등의 보안 위협을 인프라 레벨에서 원천 차단하기 위한 Kubernetes 기반 보안 API 게이트웨이입니다.

초고속 추론 성능을 제공하는 **Groq Cloud API**를 안전하게 중계하고, 모든 트래픽을 제어·암호화·모니터링하는 것을 목표로 합니다.

---

## 🏗️ 시스템 아키텍처


<img width="3393" height="2607" alt="k8s-architecture (2)" src="https://github.com/user-attachments/assets/74834101-8408-4f4c-bf5e-56dad2acacde" />


<img width="5766" height="2676" alt="제목 없는 다이어그램 drawio (7)" src="https://github.com/user-attachments/assets/ee2bf7ed-2a41-4b06-9263-92c318465ee7" />



### 레이어별 역할

| 레이어 | 구성 요소 | 역할 |
|--------|-----------|------|
| **Security Layer** | Nginx Ingress, Rate Limiting, SSL/TLS, JWT | 외부 트래픽 인증 및 암호화 종단 처리 |
| **Control Plane** | kube-apiserver, etcd, Calico CNI, Scheduler | 클러스터 상태 관리 및 네트워크 정책 제어 |
| **Data Plane** | containerd, kubelet, kube-proxy | Groq 연동 서버 및 모니터링 파드 실행 |
| **Application Layer** | FastAPI, PostgreSQL, MQTT Broker | AI API 중계, 암호화 로그 저장, IoT 데이터 수신 |
| **Observability Layer** | Prometheus, Grafana, Alertmanager | 실시간 메트릭 수집, 시각화, 이상 탐지 알림 |

---

## 🔧 기술 스택

| 분류 | 기술 |
|------|------|
| **Infra** | Kubernetes (Ubuntu 22.04), Calico CNI, Nginx Ingress Controller |
| **AI / Backend** | Groq Cloud API (groq SDK), FastAPI, Python Async |
| **Security** | Calico Network Policy, AES-256 (Fernet), JWT, Kubernetes Secret |
| **Monitoring** | Prometheus, Grafana, Alertmanager, Telegram Bot |

---

## ✨ 핵심 차별점

### 1. 지능형 트래픽 제어
Ingress 레벨의 Rate Limiting을 통해 Groq API의 초고속 호출 특성으로 인한 **비용 폭증과 API 남용을 방어**합니다.

### 2. Zero-Trust 네트워크
Calico Network Policy로 **파드 간 비인가 횡단 이동을 전면 차단**합니다. FastAPI ↔ PostgreSQL 등 명시적으로 허용된 통신 경로 외에는 모든 접근이 기본 거부됩니다.

### 3. 데이터 기밀성 보장
Groq을 통해 생성된 **모든 AI 응답 로그를 AES-256 알고리즘(Fernet)으로 즉시 암호화**하여 저장합니다. 암호화 키는 Kubernetes Secret으로 안전하게 관리됩니다.

### 4. 비동기 AI 추론 최적화
Groq 공식 Python SDK의 **비동기(Async) 요청 처리**를 활용해 초저지연 AI 응답 성능을 극대화합니다.

---

## 🔄 요청 흐름도 (Request Flow)
```
① 클라이언트 요청
   사용자 / IoT 디바이스
         │  HTTPS
         ▼
② Nginx Ingress Controller
   ├─ SSL/TLS 복호화
   ├─ Rate Limiting 검사  ─── 초과 시 ──→  [429 Too Many Requests]
   └─ 도메인 기반 라우팅
         │
         ▼
③ JWT 인증 미들웨어 (FastAPI)
   ├─ Bearer Token 검증  ──── 실패 시 ──→  [401 Unauthorized]
   └─ 토큰 만료 시간 확인
         │
         ▼
④ FastAPI 애플리케이션
   ├─ 요청 파싱 및 유효성 검사
   └─ Groq Cloud API 비동기 호출 (groq SDK)
              │
              ▼
        [Groq Cloud / LLM 추론]
              │ AI 응답 반환
              ▼
   ├─ 응답 데이터 AES-256 암호화
   └─ PostgreSQL 로그 저장 (Calico Policy 경유)
         │
         ▼
⑤ 클라이언트에 JSON 응답 반환
         │
         ▼
⑥ Prometheus 메트릭 수집
   ├─ 요청 수 / 응답 시간 / 오류율 기록
   ├─ Grafana 대시보드 시각화
   └─ 임계치 초과 시 Alertmanager → Telegram 알림
```

---

## 🔗 프로젝트 링크



| 📖 **Wiki (설계/기획/이행 문서)** | [Wiki 바로가기](https://github.com/msp-architect-2026/park-seowoo/wiki) |
| 📋 **Project 칸반보드** | [칸반보드 바로가기](https://github.com/orgs/msp-architect-2026/projects/22/views/1) |

© 2026 [parkseowoo](https://github.com/parkseowoo) · All rights reserved.
