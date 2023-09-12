from flask_app.config.mysqlconnection import connectToMySQL


class Sasq:
  DB = 'user_sasq'

  def __init__(self, data):
    self.id = data['id']
    self.user_id = data['user_id']
    self.location = data['location']
    self.whathappend = data['whathappened']
    self.numberof = data['numberof']
    self.posted_by = data.get('posted_by')
    self.made_at = data.get('made_at')

  @classmethod
  def save (cls, data):
    query = """INSERT into sasq (location, whathappened, numberof, user_id, made_at, created_at, updated_at) 
VALUES ( %(location)s, %(whathappened)s, %(numberof)s, %(user_id)s, %(made_at)s, NOW(),NOW());"""
    results = connectToMySQL('user_sasq').query_db(query, data)
    return results

  @classmethod
  def get_sasq_by_id(cls, id):
    query = """SELECT sasq.id as id, location, whathappened, numberof, made_at, sasq.created_at, sasq.updated_at, user_id, first_name AS posted_by FROM
    sasq JOIN users ON users.id = sasq.user_id WHERE sasq.id = %(id)s;"""
    results = connectToMySQL('user_sasq').query_db(query, {"id": id})
    return cls(results[0])

  @classmethod
  def get_all(cls):
    query = """SELECT sasq.id as id, location, whathappened, numberof, made_at, sasq.created_at, sasq.updated_at, user_id, first_name AS posted_by FROM
    sasq JOIN users ON users.id = sasq.user_id;"""
    results = connectToMySQL('user_sasq').query_db(query)
    if not results:
      return []
    return [cls(row) for row in results]

  @classmethod
  def edit_sasq(cls, data):
    query = """UPDATE sasq SET location=%(location)s, whathappened=%(whathappened)s, numberof=%(numberof)s, made_at=%(made_at)s WHERE sasq.id = %(id)s;"""
    results = connectToMySQL('user_sasq').query_db(query, data)
    return results

  @classmethod
  def delete_sasq_by_id(cls, id):
    query = """DELETE FROM sasq WHERE id = %(id)s;"""
    results = connectToMySQL('user_sasq').query_db(query, {"id": id})
    return results

  @staticmethod
  def validate(data):
      errors = []

      required_fields = ('location', 'whathappened', 'numberof', 'made_at')
      for required_field in required_fields:
        if required_field not in data:
          errors.append(f"Missing required field '{required_field}'!")

      if int(data['numberof']) < 1:
        errors.append("Minimum of 1 sasquatches must be sighted to report.")

      is_valid = len(errors) == 0
      return is_valid, errors