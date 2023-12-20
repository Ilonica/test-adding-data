import requests
from faker import Faker

fake = Faker('ru_RU')

def random():
    lastname, firstname, patronymic = fake.name().split()
    return {"firstname": firstname, "lastname": lastname, "patronymic": patronymic, "lastnameInitials": f"{lastname} {firstname[0]}.{patronymic[0]}."}

payload = {
  "version": "string",
  "student": {
    "personalData": random()
    }
}

updated_payload = {
"version": "string",
  "student": {
    "personalData": random()
    }
}

payload = {
  "version": "string",
  "student": {
    "personalData": {
      "firstname": "Владимир",
      "lastname": "Аристов",
      "patronymic": "Михайлович",
      "lastnameInitials": "Аристов В.М."
    }
  }
}

updated_payload = {
  "version": "string",
  "student": {
    "personalData": {
      "firstname": "Владимир",
      "lastname": "Аристов",
      "patronymic": "Михайлович",
      "lastnameInitials": "Аристов В.М."
    },
    "fgit": {
      "hasGit": True,
      "git": "https://github.com/aristov"
    },
    "fcontact": {
      "hasContact": True,
      "femail": {
        "email": "aristov@gmail.com",
        "hasEmail": True
      },
      "ftelegram": {
        "telegram": "@aristov",
        "hasTelegram": True
      },
      "fphone": {
        "phone": "89057775588",
        "hasPhone": True
      }
    }
  }
}

updated_payload_invalid = {
  "version": "string",
  "student": {
    "personalData": {
      "firstname": "Владимир",
      "lastname": "Аристов",
      "patronymic": "Михайлович",
      "lastnameInitials": "Аристов В.М."
    },
    "fgit": {
      "hasGit": True,
      "git": "123"
    },
    "fcontact": {
      "hasContact": False
    }
  }
}

BASE_URL = 'http://192.168.0.16:8080/students/general/'

response = requests.get('http://192.168.0.16:8080/students/general/2')
response = requests.post(f'{BASE_URL}', json=payload)
print(response.status_code)

BASE_URL = 'http://192.168.0.16:8080/students/general/'

# Автотесты для GET запроса
# Положительный тест: Получение информации о студенте по id
def test_get_student_by_id():
    response = requests.get(f"{BASE_URL}5")
    assert response.status_code == 200

# Отрицательный тест: Получение информации о несуществующем студенте
def test_get_nonexistent_student():
    response = requests.get(f"{BASE_URL}999")
    assert response.status_code == 201

# Деструктивный тест: Получение информации о студенте с некорректным id
def test_get_student_with_invalid_id():
    response = requests.get(f"{BASE_URL}invalid_id")
    assert response.status_code == 400

# Деструктивный тест: Получение информации о студенте, когда ответ не содержит данных
def test_get_student_with_empty_response():
    response = requests.get(f"{BASE_URL}0")
    assert response.status_code == 201

    # Проверка, на содержание в ответе ожидаемого JSON
    expected_response = {'code': 'NotFound', 'message': 'Student with id = 0 not found'}
    assert response.json() == expected_response

# Деструктивный тест: Получение информации о студенте с некорректной версией
def test_get_student_with_invalid_version():
    response = requests.get(f"{BASE_URL}2", headers={"version": "invalid_version"})
    assert response.status_code == 201


# Автотесты для PUT запроса

# Положительный тест: Добавление данных для существующего студента
def test_update_existing_student():
    # Создание студента
    response_create = requests.post(f'{BASE_URL}', json=payload)
    assert response_create.status_code >= 200 and response_create.status_code <= 299
    id = response_create.json()["info"][0]["id"]

    # Обновление персональных данных
    response_update = requests.put(f"{BASE_URL}{id}", json=updated_payload)
    assert response_update.status_code >= 200 and response_update.status_code <= 299

    # Получение студента и проверка обновлённых данных
    response_get = requests.get(f"{BASE_URL}{id}")
    assert response_get.status_code >= 200 and response_get.status_code < 299
    get_student_data = response_get.json()
    assert get_student_data["info"][0]["personalData"] == updated_payload["student"]["personalData"]


# Отрицательный тест: Добавление данных для несуществующего студента
def test_update_student_with_invalid_id():
    # Обновление данных студента с неверным id
    response_update = requests.put(f"{BASE_URL}1", json=updated_payload)
    # Ожидается, что сервер вернет код 201 Not Found и соответствующее сообщение об ошибке
    assert response_update.status_code == 201
    assert response_update.json()["code"] == "NotFound"
    assert response_update.json()["message"] == f"Student with id = 1 not found"


# Отрицательный тест: Добавление гита в некорректном формате
def test_update_invalid_git_info():
    # Создание студента
    response_create = requests.post(f'{BASE_URL}', json=payload)
    assert response_create.status_code >= 200 and response_create.status_code <= 299
    id = response_create.json()["info"][0]["id"]

    # Обновление данных с некорректной формой гита
    invalid_response_update = requests.put(f"{BASE_URL}{id}", json=updated_payload_invalid)
    assert invalid_response_update.status_code == 202

# Отрицательный тест: Добавление телефона в некорректном формате
def test_update_invalid_phone_n_info():
    # Создание студента
    payload = {
        "version": "string",
        "student": {
            "personalData": {
                "firstname": "Милана",
                "lastname": "Агаева",
                "patronymic": "Андреевна",
                "lastnameInitials": "Агаева М.А."
            }
        }
    }
    response_create = requests.post(f'{BASE_URL}', json=payload)
    assert response_create.status_code >= 200 and response_create.status_code <= 299
    id = response_create.json()["info"][0]["id"]

    updated_payload_invalid = {
  "version": "string",
  "student": {
    "personalData": {
      "firstname": "Милана",
      "lastname": "Агаева",
      "patronymic": "Андреевна",
      "lastnameInitials": "Агаева М.А."
    },
    "fgit": {
      "hasGit": False,
    },
    "fcontact": {
      "hasContact": True,
       "femail": {
          "email": "agaeva@mail.ru",
          "hasEmail": True
       },
       "ftelegram": {
          "telegram": "@agaeva",
          "hasTelegram": True
       },
       "fphone": {
          "phone": "890955",
          "hasPhone": True
        }
    }
  }
}
    # Добавление телеграма
    invalid_response_update = requests.put(f"{BASE_URL}{id}", json=updated_payload_invalid)
    assert invalid_response_update.status_code == 202

# Отрицательный тест: Добавление почты в некорректном формате
def test_update_invalid_mail_info():
    # Создание студента
    payload = {
        "version": "string",
        "student": {
            "personalData": {
                "firstname": "Милана",
                "lastname": "Агаева",
                "patronymic": "Андреевна",
                "lastnameInitials": "Агаева М.А."
            }
        }
    }
    response_create = requests.post(f'{BASE_URL}', json=payload)
    assert response_create.status_code >= 200 and response_create.status_code <= 299
    id = response_create.json()["info"][0]["id"]

    updated_payload_invalid = {
  "version": "string",
  "student": {
    "personalData": {
      "firstname": "Милана",
      "lastname": "Агаева",
      "patronymic": "Андреевна",
      "lastnameInitials": "Агаева М.А."
    },
    "fgit": {
      "hasGit": False,
    },
    "fcontact": {
      "hasContact": True,
       "femail": {
          "email": "agaeva",
          "hasEmail": True
       },
       "ftelegram": {
          "telegram": "@agaeva",
          "hasTelegram": True
       },
       "fphone": {
          "phone": "89095557788",
          "hasPhone": True
        }
    }
  }
}
    # Добавление телеграма
    invalid_response_update = requests.put(f"{BASE_URL}{id}", json=updated_payload_invalid)
    assert invalid_response_update.status_code == 202



# Деструктивный тест: Добавление очень диного телеграма в корректном формате
def test_update_long_git_info():
    # Создание студента
    payload = {
        "version": "string",
        "student": {
            "personalData": {
                "firstname": "Милана",
                "lastname": "Агаева",
                "patronymic": "Андреевна",
                "lastnameInitials": "Агаева М.А."
            }
        }
    }
    response_create = requests.post(f'{BASE_URL}', json=payload)
    assert response_create.status_code >= 200 and response_create.status_code <= 299
    id = response_create.json()["info"][0]["id"]

    updated_payload_invalid = {
  "version": "string",
  "student": {
    "personalData": {
      "firstname": "Милана",
      "lastname": "Агаева",
      "patronymic": "Андреевна",
      "lastnameInitials": "Агаева М.А."
    },
    "fgit": {
      "hasGit": False,
    },
    "fcontact": {
      "hasContact": True,
       "femail": {
          "email": "agaeva@mail.ru",
          "hasEmail": True
       },
       "ftelegram": {
          "telegram": "@agaevaagagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaaevaagaevaagaevaagaevaaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaevaagaeva",
          "hasTelegram": True
       },
       "fphone": {
          "phone": "89095557788",
          "hasPhone": True
        }
    }
  }
}
    # Добавление телеграма
    invalid_response_update = requests.put(f"{BASE_URL}{id}", json=updated_payload_invalid)
    assert invalid_response_update.status_code == 500


# Автотесты для POST запроса
# Положительный тест: Добавление студента с корректными ФИО
def test_create_student_positive():
    payload = {
        "version": "string",
        "student": {
            "personalData": {
                "firstname": "Милана",
                "lastname": "Ангелина",
                "patronymic": "Андреевна",
                "lastnameInitials": "Ангелина М.А."
            }
        }
    }
    response = requests.post(f'{BASE_URL}', json=payload)
    assert response.status_code >= 200 and response.status_code <= 299
    assert response.json()["code"] == "Ok"
    assert "info" in response.json()
    assert len(response.json()["info"]) == 1
    assert "id" in response.json()["info"][0]
    assert "personalData" in response.json()["info"][0]

# Отрицательный тест: Добавление студента с пустыми ФИО
def test_create_student_negative_missing_personal_data():
    payload = {
        "version": "string",
        "student": {
            "personalData": {
                "firstname": "",
                "lastname": "",
                "patronymic": "",
                "lastnameInitials": ""
            }
        }
    }
    response = requests.post(f'{BASE_URL}', json=payload)
    assert response.status_code == 202

# Отрицательный тест: Добавление студента без фамилии
def test_create_student_negative_invalid_firstname():
    payload = {
        "version": "string",
        "student": {
            "personalData": {
                "firstname": "",
                "lastname": "Ангелина",
                "patronymic": "Андреевна",
                "lastnameInitials": "Агаева М.А."
            }
        }
    }
    response = requests.post(f'{BASE_URL}', json=payload)
    assert response.status_code == 202

# Деструктивный тест: Добавление студента с очень длинной фамилией
def test_create_student_destructive_long_firstname():
    payload = {
        "version": "string",
        "student": {
            "personalData": {
                "firstname": "A" * 101,
                "lastname": "Ангелина",
                "patronymic": "Андреевна",
                "lastnameInitials": "Агаева М.А."
            }
        }
    }
    response = requests.post(f'{BASE_URL}', json=payload)
    assert response.status_code == 202

# Деструктивный тест: Добавление студента с неправильным названием поля
def test_create_student_destructive_invalid_payload_structure():
    payload = {
        "version": "string",
        "555": {
            "personalData": {
                "firstname": "Милана",
                "lastname": "Ангелина",
                "patronymic": "Андреевна",
                "lastnameInitials": "Агаева М.А."
            }
        }
    }
    response = requests.post(f'{BASE_URL}', json=payload)
    assert response.status_code == 500
