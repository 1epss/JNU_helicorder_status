# JNU_helicorder_status

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE) [![Supported Python versions](https://img.shields.io/badge/python-3.12.3-blue)](https://www.python.org/downloads/release/python-3123) [![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)


본 프로젝트는 **충청·전라 내륙 지진관측소의 파형 데이터**를 활용하여 **일일 자동 헬리코더(Helicorder) 시각화 시스템** 구축하는 것을 목표로 합니다.

---

## ✨ Features
- 지정 경로 내 다수의 지진파형(MSEED Format) 자동 탐색 및 시각화
- HTML 기반 Interactive Helicorder 생성 (날짜별·관측소별 검색 지원)
- 진폭 임계값 초과 시 빨간 선으로 시각적 강조
- [uv](https://github.com/astral-sh/uv) 또는 [conda](https://anaconda.org/anaconda/conda) 환경에서 간편한 설치 및 실행 지원

---

## 📦 Installation

### 1. Using uv
[uv](https://github.com/astral-sh/uv)는 빠르고 가벼운 Python 패키지 및 가상환경 관리 도구입니다.

```bash
# uv 설치
curl -LsSf https://astral.sh/uv/install.sh | sh

# 저장소 Clone
git clone https://github.com/1epss/JNU_helicorder_status.git
cd JNU_helicorder_status

# Python 3.12.3 설치
uv python install 3.12.3

# 가상환경 및 프로젝트 의존성 설치
uv sync
```

### 2. Using Conda
[conda](https://anaconda.org/anaconda/conda) 환경에서도 uv를 함께 사용할 수 있습니다.

```bash
# conda 환경 생성
conda create -n jnu-helicorder-status python=3.12.3 -y
conda activate jnu-helicorder-status

# uv 설치
pip install uv

# 프로젝트 의존성 설치
uv sync --no-venv
```

---

## 🚀 Usage

가상환경을 활성화한 후 다음 명령으로 실행합니다.

```bash
# uv를 이용한 실행
uv run python draw_helicorder_v2.py
```

또는

```bash
# uv 가상환경을 수동 활성화 후 실행
source .venv/bin/activate
python draw_helicorder_v2.py
```

실행 결과:
- 실행 후 `plots/` 내 `helicorder_<Station>_<YYYYmmdd0000>_<Component>.png` 파일이 생성됩니다.  

---

## 🧩 Scripts

### draw_helicorder_v2.py
- 지정 경로 내 저장된 지진파형(MSEED Format)으로부터 Helicorder 자동 생성
- 실행 날짜 기준 **이전 날짜(어제)** 의 데이터를 불러옴
- `crontab`을 통해 매일 오전 9시에 자동 실행되도록 설정 가능
---

### test.py (WIP)
- 특정 날짜를 지정해 Helicorder를 생성

---

### helicorder_one_station.html
- 특정 관측소, 날짜 범위, 성분(Z/N/E)을 선택하여 `plots` 경로 내 Helicorder 탐색
- 출력된 그래프 클릭 시 새 창에서 이미지로 열리며, 저장 가능

---

### helicorder_all_stations.html (WIP)
- 특정 날짜의 모든 관측소 Helicorder를 일괄 탐색

---

## 🧾 License

이 프로젝트는 **MIT 라이선스**에 따라 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참고하세요.