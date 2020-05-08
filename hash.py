from werkzeug.security import generate_password_hash, check_password_hash

if check_password_hash('pbkdf2:sha256:150000$vbuASXym$2b29121dad053e922a8730c49eb6ff0433dbec8d966f4c088684e4213a9818fc', '1234'):
    print("HASH LIKE A BOSS")

