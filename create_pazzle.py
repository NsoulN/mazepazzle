import tkinter as tk
import new_pazzle
import pannels as p

class CreatePazzle:
    def __init__(self,root):
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

        self.set_game_description() 
        self.canvas.pack()
        button = tk.Button(self.root,text="define",command=self.define)
        button.pack()

        self.cellsize = 40
        self.click_state = "white"

        self.maze = [
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0,0,0],
        ]

        self.draw_maze()

        self.player_x = 1
        self.player_y = 1
        self.player = self.canvas.create_rectangle(self.player_x*self.cellsize,
                                                    self.player_y*self.cellsize,
                                                    (self.player_x+1)*self.cellsize,
                                                    (self.player_y+1)*self.cellsize,
                                                    fill="red")
        
        self.gorl_x = 10
        self.gorl_y = 10
        self.gorl = self.canvas.create_rectangle(self.gorl_x*self.cellsize,
                                                    self.gorl_y*self.cellsize,
                                                    (self.gorl_x+1)*self.cellsize,
                                                    (self.gorl_y+1)*self.cellsize,
                                                    fill="green")
        
        self.pannels = {}

    def draw_maze(self):
        for row in range(len(self.maze)):
            for col in range(len(self.maze[0])):
                x1 = col * self.cellsize
                y1 = row * self.cellsize
                x2 = (col+1) * self.cellsize
                y2 = (row+1) * self.cellsize

                # マスを描画
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="white",
                                            tags=f"cell_{row}_{col}")

                # クリックイベントのバインディング
                self.canvas.tag_bind(f"cell_{row}_{col}", "<Button-1>", self.on_cell_click)

                #ボタンイベントのバインディング 拡張部分
                self.root.bind("<KeyPress-0>",self.road)
                self.root.bind("<KeyPress-1>",self.wall)
                self.root.bind("<KeyPress-2>",self.jump_pannel)
                self.root.bind("<KeyPress-3>",self.filter_pannel)
                self.root.bind("<KeyPress-4>",self.key_pannel)
                self.root.bind("<KeyPress-5>",self.gorl)
                self.root.bind("<KeyPress-p>",self.start)

    def on_cell_click(self, event):
        # クリックされた位置を取得
        x = event.x
        y = event.y

        # クリックされたセルの行と列を計算
        row = y // self.cellsize
        col = x // self.cellsize

        # クリックされたマスの処理（ここでは色を変更）
        if self.click_state == "black":
            if (col,row) in self.pannels:
                del self.pannels[(col,row)]
            self.maze[row][col] = 1
            self.canvas.itemconfig(f"cell_{row}_{col}", fill="black")  # 壁に変更
        elif self.click_state == "white":
            if (col,row) in self.pannels:
                del self.pannels[(col,row)]
            self.maze[row][col] = 0
            self.canvas.itemconfig(f"cell_{row}_{col}", fill="white")  # 通路に変更
        elif self.click_state == "red":#プレイヤーの初期位置を設定
            if (col,row) in self.pannels:
                del self.pannels[(col,row)]
            if self.maze[row][col] == 0:
                self.click_state = "white"
                self.player_x = col
                self.player_y = row
                self.update_player_locate()
        elif self.click_state == "green":
            if (col,row) in self.pannels:
                del self.pannels[(col,row)]
            if self.maze[row][col] == 0:
                self.click_state = "white"
                self.gorl_x = col
                self.gorl_y = row
                self.update_gorl_locate()
        elif self.click_state == "purple":
            self.pannels[(col,row)] = p.Jump_Pannel(col,row)
            self.canvas.itemconfig(f"cell_{row}_{col}", fill="purple")  # ジャンプパネルに変更
        elif self.click_state == "orange":
            self.pannels[(col,row)] = p.filter_Pannel(col,row)
            self.canvas.itemconfig(f"cell_{row}_{col}", fill="orange")  # フィルターパネルに変更
        elif self.click_state == "yellow":
            self.pannels[(col,row)] = p.key_Pannel(col,row)
            self.canvas.itemconfig(f"cell_{row}_{col}", fill="yellow")  # キーパネルに変更

    def update_player_locate(self):
        self.canvas.coords(self.player,
                            self.player_x*self.cellsize,
                            self.player_y*self.cellsize,
                            (self.player_x+1)*self.cellsize,
                            (self.player_y+1)*self.cellsize)
        
    def update_gorl_locate(self):
        self.canvas.coords(self.gorl,
                            self.gorl_x*self.cellsize,
                            self.gorl_y*self.cellsize,
                            (self.gorl_x+1)*self.cellsize,
                            (self.gorl_y+1)*self.cellsize)

    def define(self):
        data = {"maze":self.maze,"player":(self.player_x,self.player_y),"gorl":(self.gorl_x,self.gorl_y),"pannels":self.pannels}
        print(data)
        self.root.destroy()
        new_pazzle.start(data)


    def set_game_description(self):
        """ゲームの説明文を初期設定する"""
        description = """
        **説明**

        マスをクリックすることで迷路を作ることができます。
        対応するキーは以下の通りです

        **キー一覧:**
        - 0:通路（通行可能) 色：白
        - 1: 壁 (移動不可) 色：黒
        - 2: ジャンプパネル (2マス移動) 色：紫
        - 3: フィルターパネル (特定のアイテムが必要) 色：橙色
        - 4: キーパネル (フィルターパネルを通れるようになる) 色：黄色
        - 5: ゴール 色：緑
        - p: プレイヤー 色：赤
        """
        self.description_text.set(description)
    
    def road(self,event):
        self.click_state = "white"
    
    def wall(self,event):
        self.click_state = "black"

    def start(self,event):
        self.click_state = "red"
    
    def gorl(self,event):
        self.click_state = "green"

    def jump_pannel(self,event):
        self.click_state = "purple"
    
    def key_pannel(self,event):
        self.click_state = "yellow"
    
    def filter_pannel(self,event):
        self.click_state = "orange"


root = tk.Tk()
CreatePazzle(root)
root.mainloop()
