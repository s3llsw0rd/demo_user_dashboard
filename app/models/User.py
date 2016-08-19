from system.core.model import Model

class User(Model):
	def __init__(self):
		super(User, self).__init__()

	def all_users(self):
		query = 'SELECT * FROM users;'
		return self.db.query_db(query)

	def one_user(self, id):
		if not id:
			return False
		query = 'SELECT * FROM users WHERE id = :id LIMIT 1'
		data = { 'id': id }
		user = self.db.query_db(query, data)
		return user[0]

	def destroy_user(self, id):
		if not id:
			return False
		query = 'DELETE FROM users WHERE id = :id'
		data = { 'id': id }
		return self.db.query_db(query, data)

	def insert_user(self, info):
		if not 'email' in info or not 'fname' in info or not 'lname' in info or not 'password' in info:
			return False
		# VALIDATION
		query = 'INSERT INTO users (email, first_name, last_name, password, user_level) VALUES (:email, :first_name, :last_name, :password, :user_level)'
		data = {
				'email': info['email'].lower(),
				'first_name': info['fname'],
				'last_name': info['lname'],
				'password': self.bcrypt.generate_password_hash(info['password'])
		}
		if len(self.all_users()) == 0:
			data['user_level'] = 9 
		else:
			data['user_level'] = 1

		user_id = self.db.query_db(query, data)
		user = self.one_user(user_id)
		return user

	def user_login(self, info):
		if not 'email' in info or not 'password' in info:
			return False
		query = 'SELECT * FROM users WHERE email = :email'
		users = self.db.query_db(query, info)
		user = users[0]
		if user:
			if self.bcrypt.check_password_hash(user.pw_hash, info['password']):
				return user
		return False


	"""
	Below is an example of a model method that queries the database for all users in a fictitious application
	
	Every model has access to the "self.db.query_db" method which allows you to interact with the database

	def get_users(self):
		query = "SELECT * from users"
		return self.db.query_db(query)

	def get_user(self):
		query = "SELECT * from users where id = :id"
		data = {'id': 1}
		return self.db.get_one(query, data)

	def add_message(self):
		sql = "INSERT into messages (message, created_at, users_id) values(:message, NOW(), :users_id)"
		data = {'message': 'awesome bro', 'users_id': 1}
		self.db.query_db(sql, data)
		return True
	
	def grab_messages(self):
		query = "SELECT * from messages where users_id = :user_id"
		data = {'user_id':1}
		return self.db.query_db(query, data)

	"""