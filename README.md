🛡️ K8S 기반 보안 API 게이트웨이 시스템 (Secure AI Gateway)

안전한 트래픽 제어 및 Groq Cloud API 연동을 위한 클라우드 네이티브 보안 아키텍처

1. 프로젝트 개요 (Overview)
본 프로젝트는 클라우드 네이티브 환경에서 AI 서비스 확산에 따른 보안 위협(DDoS, API Key 노출 등)을 인프라 레벨에서 원천 차단하기 위한 Kubernetes 기반 보안 API 게이트웨이를 구축하는 데 목적이 있습니다. 특히 초고속 추론 성능을 제공하는 Groq Cloud API를 안전하게 중계하고 제어하는 인프라를 지향합니다.

2. 시스템 아키텍처 (System Architecture)
<img width="1342" height="1277" alt="_C__Users_EZEN_Downloads_k8s-architecture html (1)" src="https://github.com/user-attachments/assets/ab876676-7701-4778-9166-dc5d02a80493" />


[Key Layers]
Security Layer: Nginx Ingress를 통한 Rate Limiting, SSL/TLS 종단 암호화, JWT 검증 적용.

Control Plane (Master Node): kube-apiserver, etcd, Calico CNI를 통한 클러스터 및 네트워크 정책 관리.

Data Plane (Worker Node): containerd 런타임 기반의 Groq 연동 서버 및 모니터링 파드 구동.

Application Layer: FastAPI(Groq API 연동), PostgreSQL(암호화 데이터 로그), MQTT Broker 연동.

Observability Layer: Prometheus와 Grafana를 활용한 실시간 트래픽 메트릭 수집 및 이상 탐지.

3. 기술 스택 (Tech Stack)
Infra: K8s (Ubuntu 22.04), Calico CNI, Ingress Controller

AI/Backend: Groq Cloud API (groq SDK), FastAPI

Security: Calico Network Policy, AES-256 Encryption (Fernet), JWT, K8s Secret

Monitoring: Prometheus, Grafana, Alertmanager (Telegram 연동)

4. 핵심 차별점 (Core Strengths)
지능형 트래픽 제어: Ingress 수준의 Rate Limiting으로 Groq API의 초고속 호출 특성에 따른 비용 폭증 및 남용 방어.

제로 트러스트 네트워크: Calico Network Policy를 통해 API 파드와 DB 파드 간의 승인된 통신 외 모든 접근 차단.

데이터 기밀성: Groq을 통해 생성된 모든 AI 응답 로그를 AES-256 알고리즘으로 즉시 암호화하여 저장.

최신 SDK 연동: Groq 공식 Python SDK를 활용한 비동기(Async) 요청 처리로 초저지연 AI 응답 성능 극대화.

5. 현재 진행 상황 (Status)
✅ K8s 클러스터 및 Calico CNI 구축 완료

✅ Nginx Ingress Controller 및 보안 설정 완료

✅ AES-256 데이터 암호화 로직 구현 완료

✅ Groq Cloud API 연동 및 비동기 추론 성능 최적화 완료

🔲 Prometheus/Grafana 대시보드 및 알림 시스템 구축 예정

© 2026 parkseowoo. All rights reserved.
