

class UserLogin:
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self
    
    def is_authenticated(self):
        return self.__user is not None
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False
    
    def get_id(self):
        return str(self.__user['id'])
    
    @property
    def username(self):
        return self.__user['username'] if self.__user else None

    @property
    def email(self):
        return self.__user['email'] if self.__user else None