from os import system
from tabulate import tabulate
import types

clear = lambda: system('clear')

# DEFINING CLASSES
class User:
  def __init__(user, id, root_balance):
    user.id = id
    user.root_balance = root_balance

  def details(abc):
    print("User #" + str(abc.id), "|", "Root balance: " + str(abc.root_balance), '\n')

class Channel:
  def __init__(channel, id, left_user_id, left_col, left_cred, right_user_id, right_col, right_cred):
    channel.id = id
    channel.left_user_id = left_user_id
    channel.left_col = left_col
    channel.left_cred = left_cred
    channel.left_unsec = 0
    channel.left_balance = left_col + left_cred
    channel.right_user_id = right_user_id
    channel.right_col = right_col
    channel.right_cred = right_cred
    channel.right_unsec = 0
    channel.right_balance = right_col + right_cred
    channel.delta = left_col + left_cred
    channel.capacity = left_col + left_cred + right_col + right_cred
    channel.users = (left_user_id, right_user_id)

  def details(abc):
    print("Channel #" + str(abc.id) + " between users #" + str(abc.left_user_id) + " and #" + str(abc.right_user_id), '\n', "Capacity: " + str(abc.capacity), '\n', "Left user balance: " + str(abc.left_balance), '\n', "Right user balance: " + str(abc.right_balance), '\n')

class Transaction:
  def __init__(transaction, id, channel_id, delta_diff):
    transaction.id = id
    transaction.channel_id = channel_id
    transaction.delta_diff = delta_diff

  def details(abc):
    print("Transaction #" + str(abc.id), "|", "Delta diff: " + str(abc.delta_diff), '\n')

# CREATE USER
users = []
user_ids = []
def create_user(root_balance):
  if root_balance < 0:
    print("(!) Balance can't be negative.", '\n')
  else:
    id = len(users) + 1
    new_user = User(id, root_balance)
    new_user.details()
    users.append(vars(new_user))
    user_ids.append(id)

# CREATE CHANNEL
channels = []
channel_ids = []
channel_users = []

# Check if there channel between users
def check_channel(sender_id, receiver_id):
  if sender_id < receiver_id:
    left_user_id = sender_id
    right_user_id = receiver_id
  else:
    left_user_id = receiver_id
    right_user_id = sender_id
  
  if (left_user_id, right_user_id) in channel_users:
    return True
  else:
    return False

# Open channel
def open_channel():
  user1 = int(input("Enter first user ID: "))
  if user1 not in user_ids:
    print("(!) User does not exist.", '\n')
    return
  else:
    user2 = int(input("Enter second user ID: "))
    if user2 not in user_ids:
      print("(!) User does not exist.", '\n')
      return
    else:
      pass

  if user1 == user2:
    print("(!) Can't open channel with yourself.", '\n')
    return
  else:
    pass

  if check_channel(user1, user2) is True:
    print("(!) Channel is already exist.", '\n')
    return
  else:
    pass

  col1 = float(input("Enter first user collateral: "))
  cred1 = float(input("Enter first user credit: "))
  col2 = float(input("Enter second user collateral: "))
  cred2 = float(input("Enter second user credit: "))
  # print('\n')
  if any(i < 0 for i in (col1, cred1, col2, cred2)):
    print("(!) Balance values shoud be positive.", '\n')
    return
  else:
    pass

  if user1 < user2:
    left_user_id = user1
    left_col = col1
    left_cred = cred1
    right_user_id = user2
    right_col = col2
    right_cred = cred2
  else:
    left_user_id = user2
    left_col = col2
    left_cred = cred2
    right_user_id = user1
    right_col = col1
    right_cred = cred1

  for i in range(len(users)):
    if users[i]["id"] == left_user_id:
      if left_col > users[i]["root_balance"]:
        print("(!) Not enough root balance for the left user.", '\n')
        return
      else:
        pass
    if users[i]["id"] == right_user_id:
      if right_col > users[i]["root_balance"]:
        print("(!) Not enough root balance for the right user.", '\n')
        return
      else:
        pass

  id = len(channels) + 1
  new_channel = Channel(id, left_user_id, left_col, left_cred, right_user_id, right_col, right_cred)
  new_channel.details()
  channels.append(vars(new_channel))
  channel_ids.append(id)
  channel_users.append((vars(new_channel)["left_user_id"], vars(new_channel)["right_user_id"]))

# BALANCES
def update_balances(transaction_id):
  for i in range(len(transactions)):
    if transactions[i]["id"] == transaction_id:
      channel_id = transactions[i]["channel_id"]
      delta_diff = transactions[i]["delta_diff"]
    else:
      pass

  for i in range(len(channels)):
    if channels[i]["id"] == channel_id: # found channel

      if delta_diff > 0: # charge left, pay right
        if channels[i]["left_unsec"] >= abs(delta_diff):
          channels[i]["left_unsec"] = channels[i]["left_unsec"] - abs(delta_diff) # reduce unsec
          channels[i]["right_cred"] = channels[i]["right_cred"] + abs(delta_diff) # increase credit

        elif channels[i]["left_unsec"] > 0 and channels[i]["left_unsec"] < abs(delta_diff):
          delta_diff_unsec = channels[i]["left_unsec"]
          delta_diff_unsec_col = abs(delta_diff) - channels[i]["left_unsec"]
          channels[i]["left_unsec"] = channels[i]["left_unsec"] -  delta_diff_unsec # reduce unsec
          channels[i]["left_col"] = channels[i]["left_col"] - delta_diff_unsec_col # reduce collateral
          channels[i]["right_cred"] = channels[i]["right_cred"] + delta_diff_unsec # increase credit
          channels[i]["right_col"] = channels[i]["right_col"] + delta_diff_unsec_col # increase collateral
        
        elif channels[i]["left_unsec"] == 0 and channels[i]["left_col"] >= abs(delta_diff):
          channels[i]["left_col"] = channels[i]["left_col"] - abs(delta_diff) # reduce collateral
          channels[i]["right_col"] = channels[i]["right_col"] + abs(delta_diff) # increase collateral

        elif channels[i]["left_unsec"] == 0 and channels[i]["left_col"] > 0 and channels[i]["left_col"] < abs(delta_diff):
          delta_diff_col = channels[i]["left_col"]
          delta_diff_col_cred = abs(delta_diff) - channels[i]["left_col"]
          channels[i]["left_col"] = channels[i]["left_col"] -  delta_diff_col # reduce collateral
          channels[i]["left_cred"] = channels[i]["left_cred"] - delta_diff_col_cred # reduce credit
          channels[i]["right_col"] = channels[i]["right_col"] + delta_diff_col # increase collateral
          channels[i]["right_unsec"] = channels[i]["right_unsec"] + delta_diff_col_cred # increase unsec
        
        else:
          channels[i]["left_cred"] = channels[i]["left_cred"] - abs(delta_diff) # reduce credit
          channels[i]["right_unsec"] = channels[i]["right_unsec"] + abs(delta_diff) # increase unsec
      
      if delta_diff < 0: # charge right, pay left
        if channels[i]["right_unsec"] >= abs(delta_diff):
          channels[i]["right_unsec"] = channels[i]["right_unsec"] - abs(delta_diff) # reduce unsec
          channels[i]["left_cred"] = channels[i]["left_cred"] + abs(delta_diff) # increase credit

        elif channels[i]["right_unsec"] > 0 and channels[i]["right_unsec"] < abs(delta_diff):
          delta_diff_unsec = channels[i]["right_unsec"]
          delta_diff_unsec_col = abs(delta_diff) - channels[i]["right_unsec"]
          channels[i]["right_unsec"] = channels[i]["right_unsec"] -  delta_diff_unsec # reduce unsec
          channels[i]["right_col"] = channels[i]["right_col"] - delta_diff_unsec_col # reduce collateral
          channels[i]["left_cred"] = channels[i]["left_cred"] + delta_diff_unsec # increase credit
          channels[i]["left_col"] = channels[i]["left_col"] + delta_diff_unsec_col # increase collateral
        
        elif channels[i]["right_unsec"] == 0 and channels[i]["right_col"] >= abs(delta_diff):
          channels[i]["right_col"] = channels[i]["right_col"] - abs(delta_diff) # reduce collateral
          channels[i]["left_col"] = channels[i]["left_col"] + abs(delta_diff) # increase collateral

        elif channels[i]["right_unsec"] == 0 and channels[i]["right_col"] > 0 and channels[i]["right_col"] < abs(delta_diff):
          delta_diff_col = channels[i]["right_col"]
          delta_diff_col_cred = abs(delta_diff) - channels[i]["right_col"]
          channels[i]["right_col"] = channels[i]["right_col"] -  delta_diff_col # reduce collateral
          channels[i]["right_cred"] = channels[i]["right_cred"] - delta_diff_col_cred # reduce credit
          channels[i]["left_col"] = channels[i]["left_col"] + delta_diff_col # increase collateral
          channels[i]["left_unsec"] = channels[i]["left_unsec"] + delta_diff_col_cred # increase unsec
        
        else:
          channels[i]["right_cred"] = channels[i]["right_cred"] - abs(delta_diff) # reduce credit
          channels[i]["left_unsec"] = channels[i]["left_unsec"] + abs(delta_diff) # increase unsec

      channels[i]["left_balance"] = channels[i]["left_unsec"] + channels[i]["left_col"] + channels[i]["left_cred"]
      channels[i]["right_balance"] = channels[i]["right_unsec"] + channels[i]["right_col"] + channels[i]["right_cred"]
      channels[i]["delta"] = channels[i]["delta"] - delta_diff

    else:
      pass


# CREATE TRANSACTION
transactions = []
transaction_ids = []

def create_transaction(channel_id, delta_diff):
    id = len(transactions) + 1
    new_tx = Transaction(id, channel_id, delta_diff)
    new_tx.details()
    transactions.append(vars(new_tx))
    transaction_ids.append(id)

def transaction():
  sender_id = int(input("Enter User ID who send money: "))
  receiver_id = int(input("Enter User ID who receive money: "))

  if sender_id == receiver_id:
    print("(!) Can't send to yourself.", '\n')
    return
  else:
    pass
  
  if check_channel(sender_id, receiver_id) is False:
    print("(!) No channel between users.", '\n')
    return
  else:
    for i in range(len(channels)):
      print(channels[i]["users"])
      if tuple(sorted([sender_id, receiver_id])) == channels[i]["users"]:
        channel_id = channels[i]["id"]
        left_balance = channels[i]["left_balance"]
        right_balance = channels[i]["right_balance"]
    if bool(channel_id) is False:
      print("(!) Unexpected error.", '\n')
      return
    else:
      pass
    
    amount = float(input("Enter transfer amount: "))
    if amount <= 0:
      print("(!) Amount should positive.", '\n')
      return
    else:
      pass

    if sender_id < receiver_id:
      if left_balance >= amount:
        delta_diff = amount
      else:
        print("(!) Not enough balance for left user.", '\n')
        return
    else:
      if right_balance >= amount:
        delta_diff = (-1) * amount
      else:
        print("(!) Not enough balance for right user.", '\n')
        return
    
  create_transaction(channel_id, delta_diff)
  update_balances(len(transactions))
          
    
# SYSTEM FUNCTIONS
def table(abc):
  if tabulate(abc) == '':
    print("No data.", '\n')
  else:
    print(tabulate(abc, headers="keys"), '\n')

def menu():
  # print([f for f in globals().values() if type(f) == types.FunctionType])
  print("create_user(root_balance) // create a new user")
  print("open_channel() // open a new channel")
  print("table(name) // show data as table")
  print("transaction() // make transaction between users")
  print("channel_users // show all opened channels users")  
  print('\n')

# SETUP
create_user(2000)
create_user(400)
create_user(600)
# open_channel(1,100,0,3,0,900)
# create_transaction(1,20)
# create_transaction(1,-10)
# create_transaction(1,50)
# print(tabulate(users, headers="keys"), '\n')
# print(tabulate(channels, headers="keys"), '\n')
# print(tabulate(transactions, headers="keys"), '\n')

print("-=-=-=-=-=-=-=-=-=-=-=-=-", '\n')
# print(users[0]["id"])
# print(len(users))