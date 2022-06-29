import random

from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist

from datacenter.models import Mark, Schoolkid, Chastisement, Lesson, Subject, Commendation


def fix_marks(name):
	schoolkid = fetch_schoolkid(name)
	Mark.objects.filter(schoolkid=schoolkid, points__lt=4).update(points=5)


def del_chastisements(name):
	schoolkid = fetch_schoolkid(name)
	Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(name, subject_name):
	commendation_texts = [
		'Молодец!',
		'Отлично!',
		'Хорошо!',
		'Гораздо лучше, чем я ожидал!',
		'Ты меня приятно удивил!',
		'Великолепно!',
		'Прекрасно!',
		'Ты меня очень обрадовал!',
		'Именно этого я давно ждал от тебя!',
		'Сказано здорово – просто и ясно!',
		'Ты, как всегда, точен!',
		'Очень хороший ответ!',
		'Талантливо!',
		'Ты сегодня прыгнул выше головы!',
		'Я поражен!',
		'Уже существенно лучше!',
		'Потрясающе!',
		'Замечательно!',
		'Прекрасное начало!',
		'Так держать!',
		'Ты на верном пути!',
		'Здорово!',
		'Это как раз то, что нужно!',
		'Я тобой горжусь!',
		'С каждым разом у тебя получается всё лучше!',
		'Мы с тобой не зря поработали!',
		'Я вижу, как ты стараешься!',
		'Ты растешь над собой!',
		'Ты многое сделал, я это вижу!',
		'Теперь у тебя точно все получится!',
	]
	schoolkid = fetch_schoolkid(name)
	if schoolkid:
		try:
			subject = Subject.objects.get(title__contains=subject_name, year_of_study=schoolkid.year_of_study)
		except ObjectDoesNotExist:
			print(f"Не найдено ни одного урока {subject_name} у ученика {name}")
		lessons = Lesson.objects.filter(
			year_of_study=schoolkid.year_of_study,
			group_letter=schoolkid.group_letter,
			subject=subject
		)
		commendation_text = random.choice(commendation_texts)
		while True:
			lesson = random.choice(lessons)
			if not Commendation.objects.filter(created=lesson.date, subject=subject, schoolkid=schoolkid,):
				Commendation.objects.create(
					text=commendation_text,
					created=lesson.date,
					schoolkid=schoolkid,
					subject=lesson.subject,
					teacher=lesson.teacher
				)
				break


def fetch_schoolkid(name):
	try:
		schoolkid = Schoolkid.objects.get(full_name__contains=name)
		return schoolkid
	except MultipleObjectsReturned:
		print('Найдено более одной записи, уточните ФИО ученика')
	except ObjectDoesNotExist:
		print(f'Не найдено ни одного ученика "{name}"')
