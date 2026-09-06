# 목록 파일 안내

- `page-inventory.csv`: 5개 언어 479개 고유 일반 HTML 최종 URL
- `title-locations.csv`: 추가 title의 URL·소스 행·위젯 ID
- `image-inventory.csv`: 이미지 URL·alt·크기 속성과 사용 페이지
- `heading-inventory.csv`: 페이지에서 출력된 제목 요소
- `code-widget-inventory.csv`: 코드 위젯의 URL·위젯 ID·해시와 로컬 출력 조각 경로

이미지 목록의 `missing` 또는 빈 alt가 모두 오류라는 뜻은 아닙니다. 장식 이미지의 빈 alt는 접근성 측면에서 올바를 수 있으므로 실제 이미지와 역할을 보고 분류해야 합니다.

`code-widget-inventory.csv`의 `evidence` 파일은 용량과 민감정보 분리 원칙에 따라 GitHub에 넣지 않았습니다. 파일의 존재와 변경 여부는 `../data/source-evidence-manifest.csv`의 상대 경로와 SHA-256으로 추적합니다.
