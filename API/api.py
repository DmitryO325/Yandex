from flask import Blueprint, render_template, jsonify, request

from data.db_session import create_session
from data.jobs import Jobs

api = Blueprint('api', __name__, template_folder='templates', static_folder='static')


@api.route('/')
def main_page_api():
    return render_template('html.html')


@api.route('/jobs')
def api_jobs():
    db_sess = create_session()
    jobs = db_sess.query(Jobs).all()

    return jsonify(
        {
            'works':
                [item.to_dict(only=('id', 'job', 'work_size')) for item in jobs]
        }
    )


@api.route('/jobs/<int:jobs_id>', methods=['GET'])
def api_one_job(jobs_id):
    db_sess = create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)

    if not jobs:
        return jsonify({'Error': 'Job not find'})

    return jsonify(
        {
            'works':
                [jobs.to_dict(only=('id', 'job', 'work_size'))]
        }
    )


@api.route('/jobs', methods=['POST'])
def create_job():
    if not request.json:
        return jsonify({'Error': 'Empty request'})

    if not all(key in request.json for key in ['job', 'work_size']):
        return jsonify({'Error': 'Bad request'})

    db_sess = create_session()
    job = Jobs(
        job=request.json['job'],
        work_size=request.json['work_size']
    )

    db_sess.add(job)
    db_sess.commit()

    return jsonify(
        {
            'Result': 'Commit'
        }
    )


@api.route('/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_job(jobs_id):
    db_sess = create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)

    if not jobs:
        return jsonify({'Error': 'Job not found'})

    db_sess.delete(jobs)
    db_sess.commit()

    return jsonify(
        {
            'Result': 'Commit'
        }
    )
