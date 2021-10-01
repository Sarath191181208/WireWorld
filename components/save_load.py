import os 
import json 

def save(board):

    if not os.path.exists('./saveBoard.json'):
        with open('./saveBoard.json', 'a') as outfile:
            json_object = json.dumps({})
            outfile.write(json_object)

    with open('./saveBoard.json', 'r+') as outfile:

        boardState = {}
        boardState['board'] = {}
        helperDic = {}

        for row in board.cubes:
            for cube in row:

                if cube.value >= 1:
                    x, y = cube.row, cube.col
                    key = str(x)+','+str(y)
                    helperDic[key] = cube.value

        boardState['board'][0] = helperDic
        boardState['board']['rows'] = board.rows
        boardState['board']['cols'] = board.cols

        file_data = json.load(outfile)
        outfile.seek(0, 0)
        outfile.truncate()

        file_data.update(boardState)
        outfile.write(json.dumps(file_data, indent=4))

def load(board):
    if os.path.exists('./saveBoard.json'):
        data = json.load(open('./saveBoard.json'))
        data = data['board']
        if board.rows == data['rows'] and board.cols == data['cols']:
            board.clear()
            for items_ in data['0']:
                items = items_.split(',')
                x = int(items[0])
                y = int(items[1])
                board.cubes[x][y].value = data['0'][items_]
            board.draw()
