import tkinter as tk
import pannels as p

class Player:
    def __init__(self, canvas, grid_size, player_x, player_y, status, maze):
        # プレイヤーオブジェクトの初期化
        # canvas: 描画先の Canvas ウィジェット
        # grid_size: ゲームのグリッドサイズ
        # player_x: プレイヤーの初期 x 座標（グリッド単位）
        # player_y: プレイヤーの初期 y 座標（グリッド単位）
        # status: プレイヤーの初期状態
        # maze: プレイヤーが存在する迷路オブジェクト
        self.canvas = canvas
        self.grid_size = grid_size
        self.player_x = player_x
        self.player_y = player_y
        self.status = status
        self.item = []          # プレイヤーが持つアイテムのリスト
        self.action_limit = 0   # プレイヤーの行動制限（例：連続移動回数）
        self.maze = maze

        # プレイヤーの描画オブジェクトを作成（赤い四角形）
        self.player = self.canvas.create_rectangle(self.player_x * self.grid_size,
                                                    self.player_y * self.grid_size,
                                                    (self.player_x + 1) * self.grid_size,
                                                    (self.player_y + 1) * self.grid_size,
                                                    fill="red")

    def try_move(self, dx, dy):
        """指定された移動量で移動可能かチェックし、新しい座標を返す"""
        new_x, new_y = self.player_x + dx, self.player_y + dy
        if self.maze.check_canmove(new_x, new_y):
            return new_x, new_y
        return None, None

    def interact_with_pannel(self, x, y, arrow):
        """指定された座標のパネルとインタラクションを行う"""
        pannel = self.maze.get_pannel(x, y)
        if pannel:
            if pannel.check_canpassable(self.item):  # アイテムの状態も考慮
                self.player_x, self.player_y = x, y
                self.pannel_action(pannel, arrow)
                return True
            elif pannel.type == "block" and pannel.need_item:
                used_item = pannel.action(self.item)
                if used_item:
                    self.item.remove(used_item)
                    self.player_x, self.player_y = x, y
                    if pannel.isbreakable:
                        pannel.disappear(self.maze)
                    return True
                else:
                    print("必要なアイテムがありません。")
                    return False
            else:
                print("通行できません。")
                return False
        else:
            self.player_x, self.player_y = x, y
            return True

    def pannel_action(self, pannel, arrow):
        """パネル固有のアクションを実行する"""
        if pannel.type == "moving" and self.action_limit < 2:
            self.action_limit += 1
            new_dx, new_dy = pannel.action(arrow)
            self.move(new_dx, new_dy, arrow)
        elif pannel.type == "add":
            state = pannel.action()
            self.add_state(state)
        elif pannel.type == "item":
            item = pannel.action()
            self.add_item(item)
            pannel.disappear(self.maze)  # アイテム取得後はパネルを消す

    def move(self, dx, dy, arrow):
        """プレイヤーを移動させる"""
        new_x, new_y = self.try_move(dx, dy)
        if new_x is not None and new_y is not None:
            self.interact_with_pannel(new_x, new_y, arrow)
            self.update_player_position()

    def add_state(self, state):
        """プレイヤーの状態を設定"""
        self.status = state

    def check_state(self):
        """プレイヤーの状態を返す"""
        return self.status

    def add_item(self, item):
        """プレイヤーにアイテムを追加"""
        self.item.append(item)

    def check_item(self):
        """プレイヤーのアイテムリストを返す"""
        return self.item

    def update_player_position(self):
        """プレイヤーの描画位置を更新"""
        self.canvas.coords(self.player,
                           self.player_x * self.grid_size,
                           self.player_y * self.grid_size,
                           (self.player_x + 1) * self.grid_size,
                           (self.player_y + 1) * self.grid_size)

    def get_player_position(self):
        """プレイヤーの座標を返す"""
        return (self.player_x, self.player_y)

    def reset_action_rimit(self):
        """行動制限をリセット"""
        self.action_limit = 0


class Maze:
    def __init__(self, canvas, maze_data, pannels):
        # 迷路オブジェクトの初期化
        # canvas: 描画先の Canvas ウィジェット
        # maze_data: 迷路の構造を表す2次元リスト
        # pannels: 迷路に配置されるパネルの辞書 (座標: パネルオブジェクト)
        self.canvas = canvas
        self.maze_data = maze_data
        self.pannels = pannels
        self.pannels_id = {}  # パネルの描画オブジェクトIDを格納する辞書
        self.rows = len(self.maze_data)    # 迷路の行数
        self.cols = len(self.maze_data[0]) # 迷路の列数

    def draw_maze(self, grid_size):
        """迷路を描画する"""
        for row in range(self.rows):
            for col in range(self.cols):
                x1 = col * grid_size
                y1 = row * grid_size
                x2 = (col + 1) * grid_size
                y2 = (row + 1) * grid_size

                if self.maze_data[row][col] == 1:
                    # 壁を描画 (黒)
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="black")
                else:
                    # 道を描画 (白)
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="white")

        self.set_pannels(grid_size)  # パネルを配置

    def set_pannels(self, grid_size):
        """迷路にパネルを配置し、描画オブジェクトIDを保存する"""
        for (x, y), pannel_instance in self.pannels.items():
            x1 = x * grid_size
            y1 = y * grid_size
            x2 = (x + 1) * grid_size
            y2 = (y + 1) * grid_size
            pannel_id = self.canvas.create_rectangle(x1, y1, x2, y2, fill=pannel_instance.color)
            pannel_instance.set_canvas_id(pannel_id)  # パネルオブジェクトに描画IDを保存

    def check_canmove(self, x, y):
        """指定された座標が移動可能かチェックする"""
        if 0 <= x < self.cols and 0 <= y < self.rows and self.maze_data[y][x] == 0:
            return True
        return False

    def get_pannel(self, x, y):
        """指定された座標のパネルを取得する"""
        if (x, y) in self.pannels:
            print("s")
            return self.pannels[(x, y)]
        return None

    def remove_pannel(self, x, y):
        """指定された座標のパネルを削除する"""
        if (x, y) in self.pannels:
            pannel_to_remove = self.pannels.pop((x, y))
            if pannel_to_remove.canvas_id:
                self.canvas.delete(pannel_to_remove.canvas_id)  # 描画オブジェクトも削除

    def remove_pannel_by_coords(self, x, y):
        """座標を指定してパネルを削除 (Pannel クラスから呼び出す用)"""
        if (x, y) in self.pannels:
            del self.pannels[(x, y)]


class PazzleGame:
    def __init__(self, root,data):
        # パズルゲームオブジェクトの初期化
        # root: Tkinter のルートウィンドウ
        self.root = root
        self.root.title("パズル")

        # メインフレームを作成 (Canvas と説明文を配置するため)
        self.main_frame = tk.Frame(root)
        self.main_frame.pack()

        self.canvas_width = 480
        self.canvas_height = 480
        self.canvas = tk.Canvas(self.main_frame, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack(side="left")  # Canvas を左側に配置

        # 説明文を表示する Label を作成
        self.description_text = tk.StringVar()
        self.description_label = tk.Label(self.main_frame, textvariable=self.description_text, justify="left", font=("Arial", 12))
        self.description_label.pack(side="left", padx=10, anchor="nw")  # Label を左側に配置し、上詰めで表示

        self.set_game_description()  # 説明文を初期設定

        # 迷路の構成 (12x12)
        self.maze_data = data["maze"]

        self.grid_size = 40  # グリッドのサイズ
        self.pannels = data["pannels"]  # パネルの配置
        self.maze = Maze(self.canvas, self.maze_data, self.pannels)

        # 迷路を描画
        self.maze.draw_maze(self.grid_size)

        self.gorl_x,self.gorl_y = data["gorl"]
        self.canvas.create_rectangle(self.gorl_x * self.grid_size, self.gorl_y * self.grid_size, (self.gorl_x +1) * self.grid_size, (self.gorl_y +1) * self.grid_size,fill="green")  # ゴール地点を描画

        # プレイヤーオブジェクトを作成
        player_x,player_y = data["player"]
        self.player = Player(self.canvas, self.grid_size, player_x, player_y, "normal", self.maze)

        self.update_game_description() #説明文の更新

        # キーバインド設定
        self.root.bind("<KeyPress-Up>", self.move_up)
        self.root.bind("<KeyPress-Down>", self.move_down)
        self.root.bind("<KeyPress-Left>", self.move_left)
        self.root.bind("<KeyPress-Right>", self.move_right)

    def set_game_description(self):
        """ゲームの説明文を初期設定する"""
        description = """
        **ゲーム説明**

        赤い四角がプレイヤーです。
        矢印キーで移動します。

        **パネルの種類:**
        - 白: 通常の道
        - 黒: 壁 (移動不可)
        - 紫: ジャンプパネル (2マス移動)
        - オレンジ: フィルターパネル (特定のアイテムが必要)
        - 黄色: キーパネル (フィルターパネルを通れるようになる)
        - 緑: ゴール

        ゴールを目指してください！

        プレイヤーの状態：
        カギ:
        """
        self.description_text.set(description)

    def update_game_description(self):
        """ゲームの説明文を更新する"""
        description = f"""
        **ゲーム説明**

        赤い四角がプレイヤーです。
        矢印キーで移動します。

        **パネルの種類:**
        - 白: 通常の道
        - 黒: 壁 (移動不可)
        - 紫: ジャンプパネル (2マス移動)
        - オレンジ: フィルターパネル (特定のアイテムが必要)
        - 黄色: キーパネル (フィルターパネルを通れるようになる)
        - 緑: ゴール

        ゴールを目指してください！

        プレイヤーの状態：{self.player.check_state()}
        カギ:{"🗝" * self.player.check_item().count("key")}
        """
        self.description_text.set(description)

    # キーバインド
    def move_up(self, event):
        """上キーが押されたときの処理"""
        self.player.move(0, -1, "Up")
        self.player.reset_action_rimit()  # 行動制限をリセット
        self.check_goal(self.player.get_player_position())
        self.update_game_description() #説明文の更新

    def move_down(self, event):
        """下キーが押されたときの処理"""
        self.player.move(0, 1, "Down")
        self.player.reset_action_rimit()
        self.check_goal(self.player.get_player_position())
        self.update_game_description()

    def move_left(self, event):
        """左キーが押されたときの処理"""
        self.player.move(-1, 0, "Left")
        self.player.reset_action_rimit()
        self.check_goal(self.player.get_player_position())
        self.update_game_description()

    def move_right(self, event):
        """右キーが押されたときの処理"""
        self.player.move(1, 0, "Right")
        self.player.reset_action_rimit()
        self.check_goal(self.player.get_player_position())
        self.update_game_description()

    # 各種イベント
    def check_goal(self, position):
        """ゴール判定"""
        if position == (self.gorl_x, self.gorl_y):
            self.goal()

    def goal(self):
        """ゴール時の処理"""
        self.stop_movement()  # 移動を停止
        self.clear_effect()  # クリアエフェクトを表示
        self.canvas.create_text(
            480 // 2, 480 // 2,
            text="GAME CLEAR",
            font=("", 40),
            fill="yellow"
        )

    def clear_effect(self):
        """クリアエフェクトを表示 (画面を暗くする)"""
        self.canvas.create_rectangle(
            0, 0, 720, 480, fill="black", stipple="gray50"  # 黒で塗りつぶし、半透明の網掛け
        )

    def stop_movement(self):
        """プレイヤーの移動を停止する (キーバインドを解除する)"""
        self.root.unbind("<KeyPress-Up>")
        self.root.unbind("<KeyPress-Down>")
        self.root.unbind("<KeyPress-Left>")
        self.root.unbind("<KeyPress-Right>")


def start(data):
    # ゲームを実行
    root = tk.Tk()
    game = PazzleGame(root,data)
    root.mainloop()