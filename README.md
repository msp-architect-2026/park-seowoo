# 🛡️ K8S 기반 보안 API 게이트웨이 시스템 (Secure AI Gateway)
> **안전한 트래픽 제어 및 Gemini AI 연동을 위한 클라우드 네이티브 보안 아키텍처**

---

## 1. 프로젝트 개요 (Overview)
본 프로젝트는 클라우드 네이티브 환경에서 AI 서비스 확산에 따른 보안 위협(DDoS, SQL Injection, API Key 노출 등)을 인프라 레벨에서 원천 차단하기 위한 **Kubernetes 기반 보안 API 게이트웨이**를 구축하는 데 목적이 있습니다.

## 2. 시스템 아키텍처 (System Architecture)
<img width="1352" height="982" alt="{A2D753AB-F2F6-40F7-A27F-CAE95F6CF392}" src="https://github.com/user-attachments/assets/507b7714-43f5-4130-817a-7a9d357219ba" />



### [Key Layers]
* **Security Layer:** Nginx Ingress를 통한 Rate Limiting, SSL/TLS 종단 암호화, JWT 검증 및 WAF 개념 적용.
* **Control Plane (Master Node):** `kube-apiserver`, `etcd`, `Calico CNI`를 통한 클러스터 및 네트워크 정책 관리.
* **Data Plane (Worker Node):** `containerd` 런타임 기반의 애플리케이션 및 모니터링 파드 구동.
* **Application Layer:** FastAPI(AI 서비스), PostgreSQL(데이터), MQTT Broker(IoT)의 상호 작용.
* **Observability Layer:** Prometheus와 Grafana를 활용한 실시간 메트릭 수집 및 이상 탐지.

## 3. 기술 스택 (Tech Stack)
* **Infra:** K8s (Ubuntu 22.04), Calico CNI, Ingress Controller
* **AI/Backend:** **Google Gemini API (`google-genai`)**, FastAPI
* **Security:** Calico Network Policy, AES-256 Encryption, JWT, K8s Secret
* **Monitoring:** Prometheus, Grafana, Alertmanager (Telegram 연동)

## 4. 핵심 차별점 (Core Strengths)
1.  **지능형 트래픽 제어:** Ingress 수준의 Rate Limiting으로 무분별한 API 호출 방어 및 비용 최적화.
2.  **제로 트러스트 네트워크:** Calico Network Policy를 통해 파드 간의 불필요한 통신을 L3/L4 레벨에서 차단.
3.  **데이터 기밀성:** 민감한 대화 로그 및 개인정보를 AES-256 알고리즘으로 암호화하여 DB 저장.
4.  **최신 SDK 적용:** Legacy SDK 대신 최신 `google-genai` 라이브러리를 사용한 비동기 API 처리.

## 5. 현재 진행 상황 (Status)
* ✅ K8s 클러스터 및 Calico CNI 구축 완료
* ✅ Nginx Ingress Controller 및 보안 설정 완료
* ✅ AES-256 데이터 암호화 로직 구현 완료
* 🔄 **Gemini SDK (`google-genai`) 마이그레이션 및 비동기 코드 최적화 중**
* 🔲 Prometheus/Grafana 대시보드 및 알림 시스템 구축 예정

---
© 2026 parkseowoo. All rights reserved.
