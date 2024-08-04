import os
from datetime import datetime

from dotenv import load_dotenv

from file_access import FileAccess
from template_matching import TemplateMatching

# .envファイルから環境変数を読み込む
load_dotenv()

# 定数を定義（環境変数から値を取得）
NAMED_RANGES_FILE_PATH: str = os.environ["NAMED_RANGES_FILE_PATH"]
INPUT_IMAGE_FILE_PATH: str = os.environ["INPUT_IMAGE_FILE_PATH"]
INPUT_TEMPLATE_FILE_PATH: str = os.environ["INPUT_TEMPLATE_FILE_PATH"]
OUTPUT_IMAGE_DIRECTORY_PATH: str = os.environ["OUTPUT_IMAGE_DIRECTORY_PATH"]
OUTPUT_CSV_DIRECTORY_PATH: str = os.environ["OUTPUT_CSV_DIRECTORY_PATH"]
THRESHOLD: float = float(os.environ["THRESHOLD"])

if __name__ == "__main__":
    # 変数を定義
    file_access: FileAccess = FileAccess(NAMED_RANGES_FILE_PATH)
    loaded_data: dict = file_access.read_json_file()
    named_ranges: list[dict[str, str | int]] = loaded_data["namedRanges"]
    prefix: str = ""
    template_matching: TemplateMatching = TemplateMatching()

    # 画像ファイルを読み込む（image_fileが被検索対象画像、template_fileが検索対象画像）
    template_matching.load_image_files(
        image_file_path=INPUT_IMAGE_FILE_PATH,
        template_file_path=INPUT_TEMPLATE_FILE_PATH,
    )
    # 被検索対象画像の各部位と検索対象画像との類似度を計算する
    template_matching.calculate_similarities()
    # 類似度が閾値以上の場合、その座標を抽出する
    template_matching.extract_coordinates(THRESHOLD)
    # X、Y座標と検索対象画像のサイズ（横幅、高さ）を基に、範囲を算出する
    template_matching.calculate_ranges()

    # 範囲に名前をつけるための設定を格納した配列をループ処理
    for named_range in named_ranges:
        # インスタンス変数named_rangesにオブジェクトを追加する
        template_matching.append_named_range(
            name=named_range["name"],
            start_x=named_range["startX"],
            start_y=named_range["startY"],
            end_x=named_range["endX"],
            end_y=named_range["endY"],
        )

    # 範囲に名前を付与する
    template_matching.add_names_to_ranges()
    # 現在日時を出力ファイルのプレフィックスとして使用する
    prefix = datetime.now().strftime("%Y%m%d-%H%M")
    # マッチングの結果を視覚化し、画像ファイルとして保存する
    template_matching.visualize_matching_result(
        f"{OUTPUT_IMAGE_DIRECTORY_PATH}/{prefix}_matching-result.jpg"
    )
    # マッチングの結果をCSVファイルとして出力する（保存する）
    template_matching.export_matching_result_to_csv(
        f"{OUTPUT_CSV_DIRECTORY_PATH}/{prefix}_matching-result.csv"
    )
