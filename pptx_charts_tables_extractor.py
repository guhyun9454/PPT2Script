from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

def extract_charts(ppt_file_path):
    # 파워포인트 프레젠테이션 파일 로드
    presentation = Presentation(ppt_file_path)

    # 차트 데이터를 저장할 리스트
    charts_data = []

    # 프레젠테이션의 슬라이드를 순회
    for slide_num, slide in enumerate(presentation.slides, start=1):
        slide_charts = []

        # 슬라이드의 모든 쉐이프를 순회
        for shape in slide.shapes:
            # 차트 추출
            if shape.shape_type == MSO_SHAPE_TYPE.CHART:
                chart = shape.chart
                chart_data = []

                # 차트 제목 추가
                if chart.has_title:
                    chart_data.append(f"Chart Title: {chart.chart_title.text_frame.text.strip()}")

                # 차트 데이터 추출
                for series in chart.series:
                    chart_data.append(f"Series: {series.name}")
                    for point in series.points:
                        label = point.label if point.label else "No Label"
                        chart_data.append(f"  {label}: {point.value}")

                slide_charts.append("\n".join(chart_data))

        charts_data.append(slide_charts)

    return charts_data

from pptx import Presentation

def extract_tables(ppt_file_path):
    # 파워포인트 프레젠테이션 파일 로드
    presentation = Presentation(ppt_file_path)

    # 표 데이터를 저장할 리스트
    tables_data = []

    # 프레젠테이션의 슬라이드를 순회
    for slide_num, slide in enumerate(presentation.slides, start=1):
        slide_tables = []

        # 슬라이드의 모든 쉐이프를 순회
        for shape in slide.shapes:
            # 표 추출
            if shape.has_table:
                table_data = []
                table = shape.table
                for row in table.rows:
                    table_data.append(" | ".join(cell.text.strip() for cell in row.cells))
                slide_tables.append("\n".join(table_data))

        tables_data.append(slide_tables)

    return tables_data

