import flask
from flask import jsonify, make_response, request
from datetime import datetime

from data import db_session
from data.jobs import Jobs

blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=('team_leader', 'job', 'work_size',
                                    'collaborators', 'start_date', 'end_date',
                                    'is_finished'))
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['GET'])
def get_one_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.get(Jobs, jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    return jsonify(
        {
            'news': jobs.to_dict(only=('team_leader', 'job', 'work_size',
                                       'collaborators', 'start_date', 'end_date',
                                       'is_finished'))
        }
    )


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['team_leader', 'job', 'work_size',
                  'collaborators', 'start_date', 'end_date',
                  'is_finished']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    try:
        start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d %H:%M:%S')
        end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return make_response(jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400)
    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        start_date=start_date,
        end_date=end_date,
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'id': jobs.id})


@blueprint.route('/api/jobs/delete/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.get(Jobs, jobs_id)
    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['PUT'])
def edit_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).filter(Jobs.id == jobs_id).first()

    if not jobs:
        return make_response(jsonify({'error': 'Not found'}), 404)

    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)

    if 'team_leader' in request.json:
        jobs.team_leader = request.json['team_leader']
    if 'job' in request.json:
        jobs.job = request.json['job']
    if 'work_size' in request.json:
        jobs.work_size = request.json['work_size']
    if 'collaborators' in request.json:
        jobs.collaborators = request.json['collaborators']
    if 'is_finished' in request.json:
        jobs.is_finished = request.json['is_finished']
    if 'start_date' in request.json:
        try:
            jobs.start_date = datetime.strptime(request.json['start_date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400)
    if 'end_date' in request.json:
        try:
            jobs.end_date = datetime.strptime(request.json['end_date'], '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return make_response(jsonify({'error': 'Invalid date format. Use YYYY-MM-DD HH:MM:SS'}), 400)

    db_sess.commit()
    return jsonify({'success': 'OK'})
