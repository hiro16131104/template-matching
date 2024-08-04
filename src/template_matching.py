import cv2
import numpy as np
import pandas as pd
from cv2.typing import MatLike
from numpy.typing import NDArray
from pandas import DataFrame


# 画像検索するためのクラス
class TemplateMatching:
    def __init__(self) -> None:
        # 被検索対象となる画像（NumPy配列）
        self.image: MatLike = None
        # 検索対象となる画像（NumPy配列）
        self.template: MatLike = None
        # 画像同士の類似度を格納する2次元配列（行列）
        self.similarities: MatLike = None
        # 抽出したX軸の座標を格納する配列
        self.coordinates_x: NDArray[np.intp] = None
        # 抽出したY軸の座標を格納する配列
        self.coordinates_y: NDArray[np.intp] = None
        # 座標と検索対象画像のサイズを基に算出した範囲を格納する配列
        self.ranges: list[dict[str, int]] = []
        # 範囲に名前をつけるための設定を格納する配列
        self.named_ranges: list[dict[str, str | int]] = []
        # self.rangesの各要素に名前を付与したもの（成果物）を格納するための配列
        self.result_ranges: list[dict[str, str | int]] = []

    # 画像ファイルを読み込む
    def load_image_files(self, image_file_path: str, template_file_path: str) -> None:
        self.image = cv2.imread(image_file_path)
        self.template = cv2.imread(template_file_path)

    # 被検索対象画像（self.image）の各部位と検索対象画像（self.template）との類似度を計算する
    def calculate_similarities(self) -> None:
        self.similarities = cv2.matchTemplate(
            self.image, self.template, cv2.TM_CCOEFF_NORMED
        )

    # 類似度が閾値以上の場合、その座標を抽出する
    def extract_coordinates(self, threshold: float) -> None:
        # 引数のバリデーション
        if not (0.0 <= threshold <= 1.0):
            raise ValueError("引数'threshold'は、0.0〜1.0の範囲で設定してください")

        # 類似度が閾値以上の要素を抽出し、その要素のX軸とY軸の座標を取得する
        self.coordinates_y, self.coordinates_x = np.where(
            self.similarities >= threshold
        )

    # X、Y座標と検索対象画像のサイズ（横幅、高さ）を基に、範囲を算出する
    def calculate_ranges(self) -> None:
        height: int = self.template.shape[0]
        width: int = self.template.shape[1]

        # 初期化
        self.ranges = []

        # X軸、Y軸の座標が格納されている配列をループ処理する
        for x, y in zip(self.coordinates_x, self.coordinates_y):
            # 範囲の始点と終点をオブジェクトに格納する
            range: dict[str, int] = {
                "start_x": int(x),
                "start_y": int(y),
                "end_x": int(x) + width,
                "end_y": int(y) + height,
            }

            # 配列の末尾に追加する
            self.ranges.append(range)

    # self.named_rangesにオブジェクトを追加する
    def append_named_range(
        self, name: str, start_x: int, start_y: int, end_x: int, end_y: int
    ) -> None:
        self.named_ranges.append(
            {
                "name": name,
                "start_x": start_x,
                "start_y": start_y,
                "end_x": end_x,
                "end_y": end_y,
            }
        )

    # 範囲の始点及び終点の座標を基に、四角形（範囲）の各頂点の座標に変換する
    def __convert_range_to_vertices(
        self, range: dict[str, int]
    ) -> dict[str, dict[str, int]]:
        vertices: dict[str, dict[str, int]] = {
            "left_top": {"x": range["start_x"], "y": range["start_y"]},
            "right_top": {"x": range["end_x"], "y": range["start_y"]},
            "left_bottom": {"x": range["start_x"], "y": range["end_y"]},
            "right_bottom": {"x": range["end_x"], "y": range["end_y"]},
        }
        return vertices

    # self.named_rangesの情報を基に、self.rangesの要素に名前を付与する
    def add_names_to_ranges(self) -> None:
        self.result_ranges = []

        for named_range in self.named_ranges:
            # 範囲（四角形）の各頂点の座標
            named_vertices: dict[str, dict[str, int]] = (
                self.__convert_range_to_vertices(named_range)
            )

            for range in self.ranges:
                # 範囲（四角形）の各頂点の座標
                vertices: dict[str, dict[str, int]] = self.__convert_range_to_vertices(
                    range
                )
                result_range: dict[str, str | int] = {}

                # verticesの座標がnamed_verticesの座標の中に収まっていない場合は、処理をスキップ
                if not (
                    vertices["left_top"]["x"] >= named_vertices["left_top"]["x"]
                    and vertices["left_top"]["y"] >= named_vertices["left_top"]["y"]
                ):
                    continue
                if not (
                    vertices["right_top"]["x"] <= named_vertices["right_top"]["x"]
                    and vertices["right_top"]["y"] >= named_vertices["right_top"]["y"]
                ):
                    continue
                if not (
                    vertices["left_bottom"]["x"] >= named_vertices["left_bottom"]["x"]
                    and vertices["left_bottom"]["y"]
                    <= named_vertices["left_bottom"]["y"]
                ):
                    continue
                if not (
                    vertices["right_bottom"]["x"] <= named_vertices["right_bottom"]["x"]
                    and vertices["right_bottom"]["y"]
                    <= named_vertices["right_bottom"]["y"]
                ):
                    continue

                # 範囲（range）に名前を付ける
                result_range = {
                    "name": named_range["name"],
                    "start_x": range["start_x"],
                    "start_y": range["start_y"],
                    "end_x": range["end_x"],
                    "end_y": range["end_y"],
                }
                self.result_ranges.append(result_range)
                break

    # マッチングの結果（抽出の結果）を視覚化し、画像ファイルとして保存する
    def visualize_matching_result(self, saved_file_path: str) -> None:
        # 画像のコピーを作成
        copied_image: MatLike = self.image.copy()

        # self.named_rangesの範囲を点線で枠囲み
        for named_range in self.named_ranges:
            cv2.rectangle(
                copied_image,
                (named_range["start_x"], named_range["start_y"]),
                (named_range["end_x"], named_range["end_y"]),
                (54, 67, 244),
                4,
            )

        # self.result_rangesの範囲を実線で枠囲み
        for result_range in self.result_ranges:
            cv2.rectangle(
                copied_image,
                (result_range["start_x"], result_range["start_y"]),
                (result_range["end_x"], result_range["end_y"]),
                (7, 193, 255),
                4,
            )

        # マッピングした画像を保存する
        cv2.imwrite(saved_file_path, copied_image)

    # マッチングの結果（抽出の結果）をCSVファイルとして出力する（保存する）
    def export_matching_result_to_csv(self, saved_file_path: str) -> None:
        data_frame: DataFrame = pd.DataFrame(self.result_ranges)
        data_frame.to_csv(saved_file_path, index=False)
