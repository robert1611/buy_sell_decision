from sql import User, session

def find_or_create_user(data):
  if not data or 'email' not in data or not data['email']:
    return {
      'success': False,
      'message': 'Invalid Data'
    }
  user = User(**data)
  session.add(user)
  session.commit()

  return {
    'success': True,
    'user': user
  }