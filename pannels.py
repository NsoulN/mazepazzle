"""
pannelクラスのチュートリアル
新しいパネルを作りたい場合は下のPannelクラスを継承してください
また特殊な動作、状態を追加したい場合は基底クラスとなるPannelクラスの__init__にself.~~という形で追加してください
また、プレイヤーの動作はパネルごとに変えるようにしているのでパネルのタイプが新しくなる、新しく引数を増やしたいという場合などは
プレイヤークラスでのmoveメソッドを確認し、該当する部分を変更、追加を行ってください
"""
class Pannel:
    def __init__(self, x, y):
        # パネルオブジェクトの初期化
        # x: パネルの x 座標（グリッド単位）
        # y: パネルの y 座標（グリッド単位）
        self.type = "normal"      # パネルの動作の種類 (normal, moving, add, block, item)
        self.passable = True      # プレイヤーが「いつでも」通過できるかどうか
        self.color = ""         # パネルの色
        self.isbreakable = False  # パネルが壊れるかどうか
        self.x = x
        self.y = y
        self.canvas_id = None     # Canvas 上の描画オブジェクトの ID

    def check_canpassable(self, item):
        """プレイヤーがパネルを通過できるかチェックする"""
        return self.passable

    def action(self, *args):
        """パネル固有のアクションを実行する"""
        pass

    def set_canvas_id(self, canvas_id):
        """Canvas 上のオブジェクトの ID を設定"""
        self.canvas_id = canvas_id

    def disappear(self, maze):
        """パネルを迷路から消す"""
        if self.canvas_id:
            maze.canvas.delete(self.canvas_id)  # Canvas から描画を削除
            maze.remove_pannel_by_coords(self.x, self.y)  # Maze のデータ構造から削除


class Jump_Pannel(Pannel):
    def __init__(self, x, y):
        # ジャンプパネルの初期化
        super().__init__(x, y)
        self.type = "moving"
        self.color = "purple"

    def action(self, arrow):
        """プレイヤーを指定方向に2マス移動させる"""
        if arrow == "Up":
            return 0, -2
        elif arrow == "Down":
            return 0, 2
        elif arrow == "Left":
            return -2, 0
        elif arrow == "Right":
            return 2, 0


class filter_Pannel(Pannel):
    def __init__(self, x, y):
        # フィルターパネルの初期化
        super().__init__(x, y)
        self.type = "block"
        self.need_item = True    # 通過に特定のアイテムが必要
        self.passable = False    # 通常は通過できない
        self.color = "orange"
        self.isbreakable = True #壊れる
        self.need_item = 'key'  # 必要なアイテムの種類

    def check_canpassable(self, items):
        return self.passable

    def action(self, items):
        """必要なアイテムを消費して通過可能にする"""
        if self.need_item in items:
            return self.need_item
        else:
            return False


class key_Pannel(Pannel):
    def __init__(self, x, y):
        # キーパネルの初期化
        super().__init__(x, y)
        self.type = "item"    # プレイヤーにアイテムを付与するパネル
        self.color = "yellow"
        self.isbreakable = True

    def action(self):
        """プレイヤーにキーアイテムを付与する"""
        return "key"