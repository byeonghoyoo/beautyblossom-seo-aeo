# BeautyBlossom SEO·AEO Roadmap Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 검증된 검색 오류를 최소 단위로 수정할 수 있도록 관리자 원본, 페이지 대응표, 변경안, 회귀 검수와 복구 기록을 준비합니다.

**Architecture:** 공개 출력 자료와 관리자 입력 원문을 분리해 보관하고, `대응표 → 수정안 → 시험 결과 → 승인 기록`이 같은 변경 ID로 이어지도록 구성합니다. 검색 정보와 이미지 작업은 별도 작업선으로 유지하며, 라이브 아임웹 반영은 계획의 자동 실행 범위에 포함하지 않습니다.

**Tech Stack:** Git, GitHub PR, Python 3 표준 라이브러리, CSV, JSON, Markdown, Mermaid, 아임웹 관리자 읽기 전용 확인, 브라우저 수동 검수

**Spec:** `docs/00-PROJECT-BRIEF-KO.md`

## Global Constraints

- 대상 언어는 `kr`, `en`, `jp`, `cn`, `tw`이며 `th`는 제외합니다.
- 사용자 승인 없이 아임웹 저장·게시·권한 변경을 하지 않습니다.
- 실제 수정할 관리자 원문과 복원 위치를 확보하기 전 변경안을 적용하지 않습니다.
- 디자인, 메뉴, 언어 이동, FAQ, 슬라이더, 상담 기능과 로드 순서를 보호합니다.
- 신규 외부 라이브러리, 전역 타이머와 반복 DOM 탐색을 추가하지 않습니다.
- 의료 효능, 기간, 안전성, 후기와 평점은 근거와 병원 검수 없이 작성하지 않습니다.
- 검색 순위와 AI 답변 인용 증가는 보장하지 않습니다.

---

### Task 1: 변경 대상과 복구본 관리표 준비

**Files:**
- Create: `audit/inventories/admin-source-backup-index.csv`
- Create: `audit/reports/BASELINE-CAPTURE-GUIDE-KO.md`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: `audit/inventories/code-widget-inventory.csv`, 기존 관리자 설정 관찰 기록
- Produces: `change_id`, `site`, `page_url`, `admin_location`, `widget_id`, `captured_at`, `backup_path`, `restore_location`, `sha256`, `review_status` 열을 가진 복구본 색인

- [ ] **Step 1: 새 파일 요구사항을 검사하는 테스트를 추가합니다.**

`tests/test_repository.py`에 복구본 색인의 열 이름과 태국어 제외, 빈 `change_id` 금지를 검사하는 테스트를 추가합니다.

- [ ] **Step 2: 테스트가 실패하는지 확인합니다.**

Run: `python -X utf8 -m unittest discover -s tests -p "test_repository.py" -k test_admin_backup_index -v`<br>
Expected: `admin-source-backup-index.csv`가 없어 FAIL

- [ ] **Step 3: 빈 템플릿과 기준선 기록 안내서를 작성합니다.**

CSV에는 정의된 열 머리글만 넣고 추정 데이터를 만들지 않습니다. 안내서에는 PC·모바일 URL, 화면 크기, 대기 조건, 기능 확인 항목, 성능 반복 횟수 기록란과 실제 제출 금지 항목을 명시합니다.

- [ ] **Step 4: 전체 테스트를 실행합니다.**

Run: `python -X utf8 -W error::ResourceWarning -m unittest discover -s tests -v`<br>
Expected: 모든 테스트 PASS

- [ ] **Step 5: 독립 커밋으로 남깁니다.**

```bash
git add audit/inventories/admin-source-backup-index.csv audit/reports/BASELINE-CAPTURE-GUIDE-KO.md tests/test_repository.py
git commit -m "docs: add source backup and baseline templates"
```

### Task 2: 시술별 5개 언어 대응표 작성

**Files:**
- Create: `audit/inventories/multilingual-page-map.csv`
- Create: `tools/validate_page_map.py`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: `audit/inventories/page-inventory.csv`, `audit/data/validated-urls.json`
- Produces: `procedure_key`, 언어별 URL, HTTP 상태, canonical, 확인 근거와 검토 상태

- [ ] **Step 1: 대응표 스키마와 소프웨이브 기대값 테스트를 작성합니다.**

소프웨이브의 실제 경로 `kr=/139`, `en=/107`, `jp=/107`, `cn=/108`, `tw=/139`와 각 URL의 200 확인 없이는 `verified`가 될 수 없도록 검사합니다.

- [ ] **Step 2: 해당 테스트가 파일 부재로 실패하는지 확인합니다.**

Run: `python -X utf8 -m unittest discover -s tests -p "test_repository.py" -k test_multilingual_page_map -v`<br>
Expected: 대응표 또는 검증기 부재로 FAIL

- [ ] **Step 3: 대응표와 읽기 전용 검증기를 작성합니다.**

검증기는 저장된 HTTP 확인 결과와 대응표를 대조하고, 태국어 열·404 대상·빈 근거·언어 중복을 오류로 반환합니다. 네트워크 요청이나 관리자 변경은 수행하지 않습니다.

- [ ] **Step 4: 소프웨이브 행과 전체 테스트를 검증합니다.**

Run: `python -X utf8 tools/validate_page_map.py`<br>
Expected: 검증된 소프웨이브 행 PASS, 미확정 행은 `pending`으로 보고<br>
Run: `python -X utf8 -W error::ResourceWarning -m unittest discover -s tests -v`<br>
Expected: 모든 테스트 PASS

- [ ] **Step 5: 독립 커밋으로 남깁니다.**

```bash
git add audit/inventories/multilingual-page-map.csv tools/validate_page_map.py tests/test_repository.py
git commit -m "audit: add verified multilingual page map"
```

### Task 3: 복수 제목 수정 후보를 원인별로 묶기

**Files:**
- Create: `audit/inventories/title-fix-candidates.csv`
- Create: `audit/reports/TITLE-FIX-PROPOSAL-KO.md`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: `audit/inventories/title-locations.csv`, 관리자 원문 복구본 색인
- Produces: 위젯별 원인 그룹, 보존 요소, 제거 후보, 영향 범위와 복구 위치

- [ ] **Step 1: 77개 페이지와 143개 추가 제목의 보존 검사를 추가합니다.**

후보표의 집계가 감사 수치와 일치하고, 각 행에 증거 경로와 검토 상태가 있는지 검사합니다.

- [ ] **Step 2: 후보표가 없어 테스트가 실패하는지 확인합니다.**

Run: `python -X utf8 -m unittest discover -s tests -p "test_repository.py" -k test_title_fix_candidates -v`<br>
Expected: 후보표 부재로 FAIL

- [ ] **Step 3: 같은 위젯과 코드 형태를 원인별로 분류합니다.**

한국어 보톡스 `/28`, 영어 소프웨이브 `/107`, 한국어 소프웨이브 `/139`를 우선 사례로 기록합니다. 관리자 원문이 없는 항목은 수정 코드가 아니라 `backup_required` 상태로 남깁니다.

- [ ] **Step 4: 수정 제안서를 작성하고 전체 검사를 실행합니다.**

제안서에는 원문과 변경안, 제거 대상 태그, 보존할 CSS·DOM·스크립트, 예상 영향과 복구 방법을 포함합니다.

Run: `python -X utf8 -W error::ResourceWarning -m unittest discover -s tests -v`<br>
Expected: 모든 테스트 PASS

- [ ] **Step 5: 독립 커밋으로 남깁니다.**

```bash
git add audit/inventories/title-fix-candidates.csv audit/reports/TITLE-FIX-PROPOSAL-KO.md tests/test_repository.py
git commit -m "audit: group duplicate title fix candidates"
```

### Task 4: 영어 소프웨이브 시험 변경 패키지 준비

**Files:**
- Create: `changes/en-sofwave-107/before.txt`
- Create: `changes/en-sofwave-107/proposed.txt`
- Create: `changes/en-sofwave-107/rollback.txt`
- Create: `changes/en-sofwave-107/review.md`
- Create: `changes/en-sofwave-107/verification.json`

**Interfaces:**
- Consumes: 승인된 페이지 대응표, 관리자 원문 복구본, 제목 수정 제안서
- Produces: 사용자가 줄 단위로 검토할 수 있는 단일 페이지 시험 패키지

- [ ] **Step 1: 관리자 원문과 승인 상태를 확인합니다.**

`admin-source-backup-index.csv`에서 영어 `/107`의 `sha256`, `restore_location`, `review_status=approved_for_proposal`이 모두 있는지 확인합니다. 하나라도 없으면 이 Task를 중단합니다.

- [ ] **Step 2: 변경 전 원문과 최소 변경안을 분리해 기록합니다.**

잘못된 언어 연결과 불필요한 문서 제목만 대상으로 하며 CSS, UI DOM, 이벤트, 리소스 순서는 그대로 둡니다. `rollback.txt`는 `before.txt`와 바이트 단위로 같게 만듭니다.

- [ ] **Step 3: diff와 정적 검사를 실행합니다.**

Run: `git diff --no-index -- changes/en-sofwave-107/before.txt changes/en-sofwave-107/proposed.txt`<br>
Expected: 승인 대상 검색 정보 외 변경 없음<br>
Run: `python -X utf8 -m py_compile tools/prepare_repository_data.py tools/validate_page_map.py`<br>
Expected: exit 0

- [ ] **Step 4: 사용자 검토용 문서를 작성합니다.**

`review.md`에 확인된 문제, 변경 줄, 보존 영역, 예상 영향, 시험 방법과 복구 방법을 정중한 한국어로 작성합니다. 실제 아임웹 적용은 하지 않습니다.

- [ ] **Step 5: 독립 커밋으로 남깁니다.**

```bash
git add changes/en-sofwave-107
git commit -m "docs: prepare English Sofwave pilot change"
```

### Task 5: 승인된 시험의 회귀 검수 기록

**Files:**
- Modify: `changes/en-sofwave-107/verification.json`
- Create: `audit/reports/EN-SOFWAVE-107-VERIFICATION-KO.md`

**Interfaces:**
- Consumes: 사용자의 시험 승인, 동일 조건의 변경 전후 화면·기능·성능 측정값
- Produces: 통과·복구 결정을 뒷받침하는 증거 기록

- [ ] **Step 1: 승인 기록이 있는지 확인합니다.**

승인 일시와 승인 범위가 없으면 시험 적용을 시작하지 않습니다. 초안 저장이 즉시 공개되는지도 먼저 확인합니다.

- [ ] **Step 2: PC와 모바일의 같은 조건에서 화면을 비교합니다.**

페이지 상단, 변경 위젯, 메뉴, 언어 이동, FAQ, 슬라이더, 상담 링크를 확인합니다. 실제 예약·메시지·구매 제출은 하지 않습니다.

- [ ] **Step 3: 검색 출력과 성능을 비교합니다.**

title, canonical, hreflang, JSON-LD 문법과 실제 연결 URL을 확인하고, 같은 기기·네트워크·화면 조건의 반복 성능 값을 기록합니다.

- [ ] **Step 4: 실패 시 복구하고 성공 시 결과만 보고합니다.**

디자인·기능·속도 중 하나라도 악화되거나 판단할 증거가 부족하면 `rollback.txt`로 복구하고 상태를 `reverted`로 기록합니다. 통과해도 사용자 승인 없이 다른 페이지로 확대하지 않습니다.

- [ ] **Step 5: 검수 자료를 커밋합니다.**

```bash
git add changes/en-sofwave-107/verification.json audit/reports/EN-SOFWAVE-107-VERIFICATION-KO.md
git commit -m "test: record English Sofwave pilot verification"
```

### Task 6: 홈페이지·설명문·상품 경로 결정 자료 준비

**Files:**
- Create: `audit/reports/HOME-CANONICAL-DECISION-KO.md`
- Create: `audit/inventories/meta-description-review.csv`
- Create: `audit/inventories/non-content-url-review.csv`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: 5개 언어 `/`와 `/home` 비교, Search Console·네이버 자료가 제공될 경우 읽기 결과, 상품 경로 10개 관찰 기록
- Produces: 대표 홈 주소 결정 근거, 설명문 검토안, 사이트맵 제외 여부 제안

- [ ] **Step 1: 자료가 없는 판단은 `unresolved`로 남기는 테스트를 작성합니다.**

선택 canonical이나 색인 자료 없이 대표 주소가 `approved`가 되지 못하도록 검사합니다.

- [ ] **Step 2: 테스트가 실패하는지 확인한 뒤 검토표를 작성합니다.**

Run: `python -X utf8 -m unittest discover -s tests -p "test_repository.py" -k test_home_decision_requires_evidence -v`<br>
Expected: 파일 부재 또는 근거 없는 승인 상태로 FAIL

- [ ] **Step 3: 5개 언어의 결정 자료를 채웁니다.**

내부 링크, 사이트맵, 현재 canonical, 실제 색인 자료를 분리해 기록합니다. 검색 도구 접근이 없으면 결론 대신 필요한 자료를 명시합니다.

- [ ] **Step 4: 설명문과 상품 경로 제안서를 검수합니다.**

의료 문구는 병원 검수 상태를 두고, 상품 경로는 삭제가 아니라 검색 노출 목적과 아임웹 설정 가능 여부를 먼저 기록합니다.

- [ ] **Step 5: 전체 테스트 후 커밋합니다.**

Run: `python -X utf8 -W error::ResourceWarning -m unittest discover -s tests -v`<br>
Expected: 모든 테스트 PASS

```bash
git add audit/reports/HOME-CANONICAL-DECISION-KO.md audit/inventories/meta-description-review.csv audit/inventories/non-content-url-review.csv tests/test_repository.py
git commit -m "audit: add home and metadata decision records"
```

### Task 7: 구조화 데이터와 이미지 검토선 분리

**Files:**
- Create: `audit/inventories/schema-content-review.csv`
- Create: `audit/inventories/image-replacement-candidates.csv`
- Create: `audit/reports/IMAGE-REVIEW-GUIDE-KO.md`
- Modify: `tests/test_repository.py`

**Interfaces:**
- Consumes: `audit/data/summary.json`, `audit/inventories/image-inventory.csv`, 화면에서 확인한 콘텐츠와 제작일 근거
- Produces: 구조화 정보 일치 검토표와 근거가 있는 이미지 교체 후보

- [ ] **Step 1: 추정 판정을 막는 테스트를 작성합니다.**

이미지 후보에는 `visual_reason`, `date_evidence`, `rights_status`, `desktop_review`, `mobile_review`가 있어야 하며, 근거가 없는 제작일과 `AI 이미지 확정` 상태를 허용하지 않습니다.

- [ ] **Step 2: 테스트가 실패하는지 확인합니다.**

Run: `python -X utf8 -m unittest discover -s tests -p "test_repository.py" -k test_image_candidates_require_evidence -v`<br>
Expected: 후보표 부재로 FAIL

- [ ] **Step 3: 구조화 데이터와 이미지 표를 따로 작성합니다.**

스키마 표는 페이지 화면 내용과 속성의 일치 여부를 기록합니다. 이미지 표는 얼굴·손·머리카락·피부·그림자·의료 장면의 구체적인 시각 근거와 제작일 출처를 기록합니다.

- [ ] **Step 4: 전체 테스트를 실행합니다.**

Run: `python -X utf8 -W error::ResourceWarning -m unittest discover -s tests -v`<br>
Expected: 모든 테스트 PASS

- [ ] **Step 5: 독립 커밋으로 남깁니다.**

```bash
git add audit/inventories/schema-content-review.csv audit/inventories/image-replacement-candidates.csv audit/reports/IMAGE-REVIEW-GUIDE-KO.md tests/test_repository.py
git commit -m "audit: separate schema and image evidence reviews"
```

### Task 8: 최종 검수와 실행 전 인계

**Files:**
- Modify: `docs/06-REVIEW-LOG.md`
- Create: `audit/reports/EXECUTION-READINESS-KO.md`

**Interfaces:**
- Consumes: Tasks 1–7의 테스트 결과, 사용자 승인 상태, 미해결 항목
- Produces: 적용 가능·보류·복구 필요 항목이 분리된 실행 전 보고서

- [ ] **Step 1: 문서 링크와 자리표시자를 검사합니다.**

Run: `rg -n "TBD|TODO|implement later|fill in details" docs audit changes tools tests`<br>
Expected: 실행 계획의 설명 문구 외 미완성 자리표시자 0건

- [ ] **Step 2: Python과 저장소 테스트를 실행합니다.**

Run: `python -X utf8 -m compileall -q tools tests`<br>
Expected: exit 0<br>
Run: `python -X utf8 -W error::ResourceWarning -m unittest discover -s tests -v`<br>
Expected: 모든 테스트 PASS

- [ ] **Step 3: 변경 내용과 민감정보를 검사합니다.**

Run: `git diff --check origin/main...HEAD`<br>
Expected: 출력 없음, exit 0<br>
Run: `git grep -I -n -E "gho_[A-Za-z0-9_]+|BEGIN PRIVATE KEY|api[ _-]?key|password" HEAD -- . ':(exclude)docs/superpowers/plans/**'`<br>
Expected: 실제 비밀정보 일치 0건

- [ ] **Step 4: 실행 준비 보고서를 작성합니다.**

통과한 항목, 미해결 항목, 실제 적용에 필요한 사용자 승인, 복구 경로와 성과 관찰 방법을 구분합니다. “SEO 최적화 완료”나 순위 상승을 표현하지 않습니다.

- [ ] **Step 5: 최종 문서 커밋을 만들고 PR로 검토를 요청합니다.**

```bash
git add docs/06-REVIEW-LOG.md audit/reports/EXECUTION-READINESS-KO.md
git commit -m "docs: record SEO execution readiness"
git push origin HEAD
```
