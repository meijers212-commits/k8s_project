# **פרויקט שבוע 11: API לניהול אנשי קשר עם Kubernetes**

## **תוכן עניינים**

1. **מטרות הפרויקט**  
2. **סקירת הפרויקט**  
3. **דרישות פונקציונליות**  
   - 3.1 מודל הנתונים  
   - 3.2 נקודות קצה של ה-API  
4. **דרישות טכניות**
   - 4.1 מבנה הפרויקט הנדרש
   - 4.2 דרישות עיצוב המחלקות
   - 4.3 דרישות Docker
   - 4.4 דרישות Kubernetes
   - 4.5 בונוס: משתני סביבה עם קובץ .env (+10 נקודות)  
5. **דרישות Git ותיעוד**  
   - 5.1 דרישות Git  
   - 5.2 דרישות תיעוד  
6. **דרישות בדיקות**  
7. **הנחיות הגשה**  
   - 7.1 מה להגיש  
   - 7.2 רשימת בדיקה להגשה  
   - 7.3 בדיקת ההגשה שלך  
8. **לוח זמנים מומלץ**  
   - 8.1 יום 1 (6 שעות)  
   - 8.2 יום 2 (6 שעות)  
9. **משאבים**  
10. **שאלות נפוצות**  
11. **הערות חשובות**

---

## 1. מטרות הפרויקט

בהשלמת פרויקט זה, תדגים:

- **תכנות מונחה עצמים** – עיצוב ומימוש מחלקות Python  
- **פעולות מסד נתונים NoSQL** – עבודה עם MongoDB באמצעות PyMongo  
- **פיתוח API** – יצירת נקודות קצה REST עם FastAPI  
- **קונטיינריזציה** – בניית תמונות Docker עבור האפליקציה שלך  
- **תזמור קונטיינרים** – פריסת אפליקציות עם Pods ו-Services של Kubernetes

---

## 2. סקירת הפרויקט

תבנה **API לניהול אנשי קשר** – שירות REST API המאפשר למשתמשים לנהל רשימת אנשי קשר. האפליקציה:

- תאחסן אנשי קשר במסד נתונים MongoDB  
- תספק נקודות קצה HTTP לפעולות CRUD (יצירה, קריאה, עדכון, מחיקה)  
- תרוץ כקונטיינרים המתוזמרים על ידי Kubernetes  
- תשתמש ב-Kubernetes Services לתקשורת רשת בין הרכיבים

**מחסנית טכנולוגית:**

- Python 3.11+  
- FastAPI (מסגרת אינטרנט)  
- MongoDB 7.0 (מסד נתונים)  
- Docker (קונטיינריזציה)  
- Kubernetes (תזמור)

**משך:** יומיים

---

## 3. דרישות פונקציונליות

### 3.1 מודל הנתונים

לכל איש קשר חייבים להיות השדות הבאים:

| שדה | סוג | אילוצים |
| :---- | :---- | :---- |
| _id | ObjectId | מפתח ראשי (נוצר אוטומטית) |
| first_name | מחרוזת (50 תווים) | חובה |
| last_name | מחרוזת (50 תווים) | חובה |
| phone_number | מחרוזת (20 תווים) | חובה, ייחודי |

### 3.2 נקודות קצה של ה-API

ה-API שלך חייב לממש 4 נקודות קצה אלו:

| מתודה | נקודת קצה | תיאור | גוף הבקשה | תגובה |
| :---- | :---- | :---- | :---- | :---- |
| GET | `/contacts` | קבל את כל אנשי הקשר | ללא | רשימת כל אנשי הקשר |
| POST | `/contacts` | צור איש קשר חדש | נתוני איש קשר | הודעת הצלחה + ID |
| PUT | `/contacts/{id}` | עדכן איש קשר קיים | שדות מעודכנים | הודעת הצלחה |
| DELETE | `/contacts/{id}` | מחק איש קשר | ללא | הודעת הצלחה |

**דוגמת בקשה/תגובה:**

```
# יצירת איש קשר
POST /contacts
{
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "050-1234567"
}

# תגובה
{
    "message": "Contact created successfully",
    "id": "507f1f77bcf86cd799439011"
}
```

---

## 4. דרישות טכניות

### 4.1 מבנה הפרויקט הנדרש

```
week11_k8s_contacts/
├── .gitignore
├── README.md
├── app/
│   ├── .env                     # משתני סביבה (אופציונלי - ראה בונוס)
│   ├── .env.example             # תבנית סביבה (אופציונלי - ראה בונוס)
│   ├── Dockerfile
│   ├── main.py                  # אפליקציית FastAPI
│   ├── data_interactor.py       # חיבור MongoDB + פעולות CRUD
│   └── requirements.txt
└── k8s/
    ├── mongodb-pod.yaml         # הגדרת Pod של MongoDB
    ├── mongodb-service.yaml     # הגדרת Service של MongoDB
    ├── api-pod.yaml             # הגדרת Pod של ה-API
    └── api-service.yaml         # הגדרת Service של ה-API
```

**הערה:** קבצי `.env` ו-`.env.example` הם אופציונליים וקשורים לדרישת הבונוס למטה.

### 4.2 דרישות עיצוב המחלקות

עליך לממש את הבאים:

1. **מחלקת Contact**  
     
   - מאפיינים: id, first_name, last_name, phone_number  
   - מתודה להמרת איש קשר לפורמט מילון

2. **מחלקה/מודול Data Interactor** (`data_interactor.py`)  
     
   קובץ זה צריך לטפל **גם** בחיבור ל-MongoDB **וגם** בכל פעולות ה-CRUD:  
     
   - יצירת חיבור MongoDB (באמצעות משתני סביבה עבור host/port)  
   - `create_contact(contact_data: dict)` → מחזיר את ה-ID של איש הקשר החדש כמחרוזת  
   - `get_all_contacts()` → מחזיר רשימת אובייקטי Contact  
   - `update_contact(id: str, contact_data: dict)` → מחזיר בוליאני של הצלחה  
   - `delete_contact(id: str)` → מחזיר בוליאני של הצלחה

3. **אפליקציית FastAPI** (`main.py`)  
     
   - הגדרת מודלי בקשה/תגובה באמצעות Pydantic  
   - מימוש 4 נקודות קצה של API  
   - טיפול בשגיאות עם קודי סטטוס HTTP מתאימים

### 4.3 דרישות Docker

**Dockerfile של האפליקציה** (`app/Dockerfile`)

- תמונת בסיס: `python:3.11-slim`  
- התקנת תלויות מ-requirements.txt  
- העתקת קוד האפליקציה  
- חשיפת פורט 8000  
- הרצת שרת uvicorn

**דוגמת Dockerfile:**

```dockerfile
FROM python:3.11-slim  
WORKDIR /app  
COPY requirements.txt .  
RUN pip install --no-cache-dir -r requirements.txt  
COPY . .  
EXPOSE 8000  
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**בנייה ודחיפה:**

לאחר יצירת ה-Dockerfile שלך, תצטרך:
1. לבנות את תמונת ה-Docker עם תג מתאים (כולל שם המשתמש שלך ב-Docker Hub)
2. להתחבר ל-Docker Hub
3. לדחוף את התמונה לרג'יסטרי של Docker Hub שלך

**הערה:** ודא שיש לך חשבון Docker Hub ושאתה מחובר לפני הדחיפה. תתייחס לתמונה זו ב-manifest של ה-Kubernetes Pod שלך.

### 4.4 דרישות Kubernetes

עליך ליצור **4 קבצי YAML** – שני Pods ושני Services. חקור manifests של Kubernetes Pod ו-Service כדי לבנות קבצים אלו.

#### 1. MongoDB Pod (`k8s/mongodb-pod.yaml`)

צור manifest של Pod עבור MongoDB עם הדרישות הבאות:

- **גרסת API**: v1
- **Kind**: Pod
- **Metadata**:
  - שם: `mongodb`
  - Labels: כלול `app: mongodb` (משמש ע"י selector של Service)
- **מפרט הקונטיינר**:
  - שם קונטיינר: `mongodb`
  - תמונה: `mongo:7.0` (תמונת MongoDB רשמית)
  - פורט קונטיינר: `27017` (פורט ברירת המחדל של MongoDB)
  - משתני סביבה:
    - `MONGO_INITDB_DATABASE` מוגדר ל-`"contactsdb"`

**מטרה:** Pod זה מריץ קונטיינר MongoDB שיאחסן את נתוני אנשי הקשר שלך.

#### 2. MongoDB Service (`k8s/mongodb-service.yaml`)

צור manifest של Service עבור MongoDB עם הדרישות הבאות:

- **גרסת API**: v1
- **Kind**: Service
- **Metadata**:
  - שם: `mongodb-service`
- **מפרט ה-Service**:
  - Selector: `app: mongodb` (מתאים ל-label של ה-Pod)
  - Port: `27017`
  - Target port: `27017`
  - Type: `ClusterIP` (גישה פנימית בלבד)

**מטרה:** Service זה מספק נקודת קצה רשת יציבה עבור MongoDB. ה-API שלך יתחבר באמצעות שם ה-host `mongodb-service`.

#### 3. API Pod (`k8s/api-pod.yaml`)

צור manifest של Pod עבור ה-API שלך עם הדרישות הבאות:

- **גרסת API**: v1
- **Kind**: Pod
- **Metadata**:
  - שם: `api`
  - Labels: כלול `app: api` (משמש ע"י selector של Service)
- **מפרט הקונטיינר**:
  - שם קונטיינר: `api`
  - תמונה: `<your-dockerhub-username>/contacts-api:v1` (החלף בשם המשתמש שלך ב-Docker Hub)
  - מדיניות משיכת תמונה: `Always` (מבטיח ש-Kubernetes ימשוך מהרג'יסטרי)
  - פורט קונטיינר: `8000`
  - משתני סביבה (קריטי - ה-API צריך אותם להתחבר ל-MongoDB):
    - `MONGO_HOST` מוגדר ל-`"mongodb-service"`
    - `MONGO_PORT` מוגדר ל-`"27017"`
    - `MONGO_DB` מוגדר ל-`"contactsdb"`

**מטרה:** Pod זה מריץ את אפליקציית FastAPI שלך. משתני הסביבה אומרים ל-API שלך איך להתחבר ל-MongoDB.

#### 4. API Service (`k8s/api-service.yaml`)

צור manifest של Service עבור ה-API שלך עם הדרישות הבאות:

- **גרסת API**: v1
- **Kind**: Service
- **Metadata**:
  - שם: `api-service`
- **מפרט ה-Service**:
  - Selector: `app: api` (מתאים ל-label של ה-Pod)
  - Port: `8000`
  - Target port: `8000`
  - Node port: `30080` (פורט גישה חיצונית)
  - Type: `NodePort` (מאפשר גישה חיצונית)

**מטרה:** Service זה חושף את ה-API שלך לעולם החיצון, והופך אותו לנגיש מהדפדפן שלך או מפקודות curl.

**משאבים ליצירת YAML:**
- Kubernetes Pods: https://kubernetes.io/docs/concepts/workloads/pods/
- Kubernetes Services: https://kubernetes.io/docs/concepts/services-networking/service/
- הפניית תחביר YAML: https://kubernetes.io/docs/reference/

### 4.5 דרישת בונוס: משתני סביבה עם קובץ .env (+10 נקודות)

**בונוס:** במקום לכתוב משתני סביבה בקוד, השתמש בקובץ `.env` לפיתוח מקומי.

**דרישות:**

1. **צור קובץ `app/.env`** עם משתני סביבה:
   ```
   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGO_DB=contactsdb
   ```

2. **טען משתני סביבה** ב-`data_interactor.py` שלך:
   - השתמש בספרייה כמו `python-dotenv` לטעינת משתנים מקובץ `.env`
   - הוסף `python-dotenv` ל-`requirements.txt` שלך
   - המשתנים צריכים להיטען אוטומטית בהרצה מקומית

3. **הוסף `.env` ל-.gitignore** (אל תעלה קובץ .env ל-commit)

4. **צור קובץ `.env.example`** עם תבנית (ללא ערכים רגישים):
   ```
   MONGO_HOST=localhost
   MONGO_PORT=27017
   MONGO_DB=contactsdb
   ```

**למה זה שימושי:**
- מפריד קונפיגורציה מקוד
- מקל על מעבר בין סביבות מקומיות וייצור
- עוקב אחר שיטות עבודה מומלצות לקונפיגורציית אפליקציות

**הערה:** בהרצה ב-Kubernetes, משתני הסביבה של ה-Pod (המוגדרים ב-`api-pod.yaml`) ידרסו את ערכי קובץ ה-`.env`.

---

## הבנת הארכיטקטורה

**מושגי מפתח:**

1. **Pods** הם יחידות הפריסה הקטנות ביותר – הם מריצים את הקונטיינרים שלך  
2. **Services** מספקים רשת יציבה – Pods יכולים לבוא וללכת, אבל שמות Services נשארים קבועים  
3. **ClusterIP** Services הם פנימיים בלבד (MongoDB לא צריך גישה חיצונית)  
4. **NodePort** Services נגישים מבחוץ (כך שתוכל לקרוא ל-API שלך)

---

## 5. דרישות Git ותיעוד

### 5.1 דרישות Git

1. **הקמת Repository**

   - צור repository ב-GitHub בשם `week11_k8s_contacts`
   - כלול `.gitignore` שמחריג:
     - `__pycache__/`
     - `*.pyc`
     - `.env`

2. **אסטרטגיית ענפים** (**חובה**)

   עליך להשתמש בזרימת עבודה של שני ענפים:

   - **ענף `main`**: קוד מוכן לייצור בלבד
     - ענף זה צריך להכיל רק קוד יציב ונבדק
     - ההגשה הסופית צריכה להיות בענף זה

   - **ענף `development`**: עבודת פיתוח פעילה
     - צור ענף זה מ-`main`
     - בצע את כל עבודת הפיתוח שלך בענף זה
     - בצע commit לעתים קרובות תוך כדי עבודה
     - כאשר התכונות מושלמות ונבדקות, מזג ל-`main`

   **זרימת עבודה:**
   1. צור ועבור לענף `development`
   2. פתח ובצע commit לקוד שלך ב-`development`
   3. בדוק הכל ביסודיות ב-`development`
   4. כשמוכן, מזג את `development` לתוך `main`
   5. הגש את ה-repository עם שני הענפים גלויים

3. **תקני Commit**

   - הודעות commit ברורות המתארות מה השתנה
   - בצע commit לעתים קרובות (במיוחד בענף `development`)

4. **זרימת Commit מוצעת**  
     
   - "Initial project structure"  
   - "Implement Contact class"  
   - "Add MongoDB connection and CRUD operations"  
   - "Implement API endpoints"  
   - "Add Dockerfile"  
   - "Add Kubernetes manifests"  
   - "Add documentation"

### 5.2 דרישות תיעוד

קובץ `README.md` שלך חייב לכלול:

1. **תיאור הפרויקט** – מה הפרויקט עושה + נקודות קצה של API  
     
2. **דרישות מקדימות:**  
     
   - Docker  
   - minikube (או Kubernetes מקומי אחר)  
   - kubectl

3. **הוראות התקנה** – איך לבנות ולפרוס  
     
4. **הוראות בדיקה** – פקודות curl לכל נקודת קצה

---

## 6. דרישות בדיקות

עליך לבדוק ולאמת:

1. **Pods רצים**

   - ודא ששני ה-pods בסטטוס "Running"
   - בדוק ש-pod ה-MongoDB מתחיל בהצלחה
   - בדוק ש-pod ה-API מתחיל בהצלחה

2. **Services נוצרו**

   - ודא ש-mongodb-service קיים ונגיש
   - ודא ש-api-service קיים ונגיש
   - אשר ש-services מנתבים תעבורה ל-pods הנכונים

3. **פעולות CRUD**

   - בדוק נקודת קצה GET לאחזור כל אנשי הקשר
   - בדוק נקודת קצה POST ליצירת איש קשר חדש
   - בדוק נקודת קצה PUT לעדכון איש קשר קיים
   - בדוק נקודת קצה DELETE להסרת איש קשר
   - כל 4 נקודות הקצה צריכות לעבוד נכון

4. **טיפול בשגיאות**

   - עדכון איש קשר לא קיים מחזיר 404
   - מחיקת איש קשר לא קיים מחזיר 404

---

## 7. הנחיות הגשה

### 7.1 מה להגיש

הגש את כתובת ה-GitHub repository שלך דרך MOODLE.

### 7.2 רשימת בדיקה להגשה

- [ ] ה-Repository ציבורי ונגיש
- [ ] ל-Repository יש גם ענף `main` וגם ענף `development`
- [ ] קוד יציב סופי נמצא בענף `main`
- [ ] README.md מכיל הוראות התקנה ובדיקה
- [ ] קובץ .gitignore קיים וכולל `.env`
- [ ] כל הקבצים הנדרשים נמצאים
- [ ] תמונת Docker נבנית בהצלחה
- [ ] כל 4 manifests של Kubernetes תקפים
- [ ] כל 4 נקודות הקצה של ה-API עובדות נכון

### 7.3 בדיקת ההגשה שלך

לפני ההגשה, בדוק את הפרויקט שלך מקצה לקצה:

1. **שכפל את ה-repository שלך** לתיקייה נקייה

2. **בנה ודחוף תמונת Docker** לרג'יסטרי Docker Hub שלך

3. **הפעל את אשכול ה-Kubernetes שלך** (minikube או אחר)

4. **פרוס את כל המשאבים** ל-Kubernetes:
   - פרוס MongoDB Pod
   - פרוס MongoDB Service
   - פרוס API Pod
   - פרוס API Service

5. **המתן שה-pods יהיו מוכנים** (בדרך כלל 30-60 שניות)
   - ודא ששני ה-pods מציגים סטטוס "Running"

6. **קבל את כתובת ה-API** מאשכול ה-Kubernetes שלך

7. **בדוק את כל נקודות הקצה של CRUD:**
   - בדוק GET /contacts (צריך להחזיר רשימה ריקה בהתחלה)
   - בדוק POST /contacts ליצירת איש קשר חדש
   - בדוק GET /contacts שוב (צריך להציג את איש הקשר שנוצר)
   - בדוק PUT /contacts/{id} לעדכון איש הקשר
   - בדוק DELETE /contacts/{id} להסרת איש הקשר

8. **אמת טיפול בשגיאות:**
   - נסה לעדכן איש קשר לא קיים (צריך להחזיר 404)
   - נסה למחוק איש קשר לא קיים (צריך להחזיר 404)

9. **נקה משאבים** כשסיימת לבדוק

---

## 8. לוח זמנים מומלץ

### 8.1 יום 1 (6 שעות)

**שעות 1-2: הקמה ושכבת מסד נתונים**

- צור GitHub repository
- צור ענף `development` ועבור אליו
- הקם מבנה פרויקט
- ממש מחלקת Contact
- ממש data_interactor.py עם חיבור MongoDB ו-CRUD
- בצע commit לעבודה שלך בענף `development`

**שעות 3-4: פיתוח API**

- צור requirements.txt  
- ממש אפליקציית FastAPI  
- ממש את כל 4 נקודות הקצה  
- בדוק מקומית (הרץ MongoDB ב-Docker, API מקומית)

**שעות 5-6: Dockerize**

- צור Dockerfile
- בנה ובדוק תמונת Docker
- בדוק קונטיינר API עם קונטיינר MongoDB

### 8.2 יום 2 (6 שעות)

**שעות 1-2: יסודות Kubernetes**

- הפעל את אשכול ה-Kubernetes שלך
- צור mongodb-pod.yaml ו-mongodb-service.yaml
- פרוס וודא ש-MongoDB רץ

**שעות 3-4: פרוס API**

- בנה ודחוף תמונה לרג'יסטרי Docker Hub
- צור api-pod.yaml ו-api-service.yaml
- פרוס ובדוק API

**שעות 5-6: בדיקות ותיעוד**

- בדוק את כל נקודות הקצה ביסודיות
- השלם README.md
- בדיקה סופית בענף `development`
- מזג ענף `development` לענף `main`
- ודא שהכל עובד בענף `main`
- דחוף את שני הענפים ל-GitHub
- הגש כתובת repository

---

## 9. משאבים

### חומר מומלץ

- יסודות FastAPI: [https://fastapi.tiangolo.com/tutorial/first-steps/](https://fastapi.tiangolo.com/tutorial/first-steps/)  
- מדריך PyMongo: [https://pymongo.readthedocs.io/en/stable/tutorial.html](https://pymongo.readthedocs.io/en/stable/tutorial.html)  
- Kubernetes Pods: [https://kubernetes.io/docs/concepts/workloads/pods/](https://kubernetes.io/docs/concepts/workloads/pods/)  
- Kubernetes Services: [https://kubernetes.io/docs/concepts/services-networking/service/](https://kubernetes.io/docs/concepts/services-networking/service/)  
- התחלת minikube: [https://minikube.sigs.k8s.io/docs/start/](https://minikube.sigs.k8s.io/docs/start/)

### קטעי קוד לדוגמה

**חיבור MongoDB ב-data_interactor.py:**

```python
import os
from pymongo import MongoClient

# קרא ממשתני סביבה (מוגדרים ב-Kubernetes Pod)
MONGO_HOST = os.getenv("MONGO_HOST", "localhost")
MONGO_PORT = os.getenv("MONGO_PORT", "27017")
MONGO_DB = os.getenv("MONGO_DB", "contactsdb")

# צור חיבור
client = MongoClient(f"mongodb://{MONGO_HOST}:{MONGO_PORT}/")
db = client[MONGO_DB]
contacts_collection = db["contacts"]
```

**המרת ObjectId לתגובות API:**

```python
from bson import ObjectId

def contact_to_dict(contact):
    return {
        "id": str(contact["_id"]),  # המר ObjectId למחרוזת
        "first_name": contact["first_name"],
        "last_name": contact["last_name"],
        "phone_number": contact["phone_number"]
    }
```

---

## 10. שאלות נפוצות

**ש: האם אני יכול להשתמש ב-Kubernetes של Docker Desktop במקום minikube?**
ת: כן! רק וודא להתאים את מדיניות משיכת התמונה ושיטת הגישה בהתאם.

**ש: מה אם ה-API שלי לא מצליח להתחבר ל-MongoDB?**
ת: בדוק ש:

1. pod ה-MongoDB רץ (אמת סטטוס pod)
2. service ה-MongoDB קיים (אמת סטטוס service)
3. ה-API שלך משתמש ב-`mongodb-service` כ-host (לא `localhost`)
4. שני ה-pods באותו namespace (default)

**ש: איך אני רואה לוגים אם משהו לא עובד?**
ת: השתמש בפקודה המתאימה לצפייה בלוגים של pod עבור גם ה-API וגם ה-MongoDB pods.

**ש: ה-API pod שלי ממשיך לקרוס. איך אני מדבג?**
ת: בדוק את לוגי ה-pod ותאר את ה-pod כדי לראות מידע מפורט על הסטטוס שלו וכל שגיאות.

**ש: האם אני צריך להשתמש ב-Deployments במקום Pods?**
ת: לפרויקט זה, Pods פשוטים מספיקים. Deployments מוסיפים תכונות כמו הפעלה מחדש אוטומטית וסקיילינג, אבל מוסיפים מורכבות.

**ש: האם הנתונים שלי יישמרו אם אמחק את pod ה-MongoDB?**
ת: לא. ללא PersistentVolume, הנתונים אובדים כאשר ה-pod נמחק. זה מקובל לפרויקט למידה זה.

**ש: האם אני יכול להריץ את ה-API מקומית (לפיתוח) אבל להתחבר ל-MongoDB ב-Kubernetes?**
ת: כן! יש לך שתי אפשרויות:

1. **Port Forwarding (מומלץ):** צור מנהרה מה-localhost שלך ל-service ה-MongoDB ב-Kubernetes על פורט 27017. אז הגדר `MONGO_HOST=localhost` בהרצת ה-API מקומית.

2. **NodePort Service:** שנה את `mongodb-service.yaml` להשתמש ב-`type: NodePort` עם nodePort (למשל, 30017). קבל את כתובת ה-IP של האשכול שלך והגדר `MONGO_HOST=<cluster-ip>` ו-`MONGO_PORT=30017`.

Port forwarding פשוט יותר כי הוא לא דורש שינוי קבצי YAML שלך.

---

## 11. הערות חשובות

### פיתוח מקומי עם Kubernetes MongoDB

**חשוב:** אם אתה רוצה להריץ את ה-API שלך מקומית (בסביבת הפיתוח שלך) בזמן התחברות ל-MongoDB הרץ ב-Kubernetes, **חייב** ליצור מנהרה או לחשוף את service ה-MongoDB. כברירת מחדל, Kubernetes services נגישים רק בתוך האשכול.

**שתי אפשרויות:**

1. **Port Forwarding (יצירת מנהרה):**
   - צור מנהרת port-forward מה-localhost שלך ל-service ה-MongoDB ב-Kubernetes
   - זה הופך את service ה-MongoDB לנגיש ב-`localhost:27017`
   - סשן ה-port-forward חייב להישאר פעיל בטרמינל בזמן שאתה מפתח

2. **NodePort (חשיפה דרך Cluster IP):**
   - שנה את סוג service ה-MongoDB מ-`ClusterIP` ל-`NodePort`
   - זה קושר פורט (טווח 30000-32767) על צומת האשכול שנגיש ממכונת ה-host שלך
   - גש ל-MongoDB באמצעות כתובת ה-IP של האשכול וה-NodePort
   - תצטרך למצוא את כתובת ה-IP של האשכול שלך

**הערה:** להגשת המטלה, השתמש בקונפיגורציית ClusterIP הסטנדרטית (גם API וגם MongoDB רצים ב-Kubernetes). הנ"ל רק לפיתוח/בדיקה מקומית.

### טעויות נפוצות להימנע מהן

❌ שימוש ב-`localhost` כ-host של MongoDB **כאשר גם API וגם MongoDB ב-Kubernetes** (השתמש ב-`mongodb-service`)
❌ שכחה להחיל את ה-Service לפני בדיקת קישוריות
❌ אי המתנה ל-pods להיות רצים לחלוטין לפני בדיקה
❌ אי דחיפת תמונת Docker לרג'יסטרי לפני פריסה
❌ שימוש בשם משתמש Docker Hub שגוי בהפניית התמונה
❌ ניסיון לחבר API מקומי ל-MongoDB ב-Kubernetes ללא port-forward או NodePort

✅ תמיד בדוק סטטוס pod לפני בדיקה
✅ השתמש בלוגי pod לדיבוג בעיות
✅ בדוק service ה-MongoDB קודם לפני פריסת API
✅ ודא שאתה מחובר ל-Docker Hub לפני דחיפה
✅ בצע commit לקוד באופן קבוע
✅ השתמש ב-port forwarding אם בודק API מקומית עם K8s MongoDB

### הערות לגבי פקודות

סטודנטים צריכים לחקור ולכלול את פקודות ה-CLI המתאימות ב-README.md שלהם עבור:

**פקודות Docker:**
- התחברות ל-Docker Hub
- בניית תמונות Docker
- דחיפת תמונות לרג'יסטרי

**פקודות Kubernetes:**
- החלה/יצירת משאבים מקבצי YAML
- קבלת/רשימת משאבים (pods, services)
- צפייה בלוגי pod
- תיאור משאבים לדיבוג
- מחיקת משאבים

**פקודות Minikube:**
- הפעלה/עצירת אשכול
- קבלת כתובות URL של service
- קבלת כתובת IP של אשכול

**פקודות בדיקה:**
- ביצוע בקשות HTTP לבדיקת נקודות קצה API (GET, POST, PUT, DELETE)

עיין בתיעוד רשמי:
- Docker CLI: https://docs.docker.com/engine/reference/commandline/cli/
- kubectl: https://kubernetes.io/docs/reference/kubectl/
- minikube: https://minikube.sigs.k8s.io/docs/commands/

---

בהצלחה! התחל עם הרצת MongoDB קודם, ואז הוסף את ה-API. בדוק בכל שלב!
