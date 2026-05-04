from flask import jsonify, abort
from flask_restful import Resource, reqparse
from data import db_session
from data.jobs import Jobs
from datetime import datetime


def abort_if_job_not_found(job_id):
    session = db_session.create_session()
    job = session.query(Jobs).get(job_id)
    if not job:
        abort(404, message=f"Job {job_id} not found")


class JobsResource(Resource):
    def get(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.get(Jobs, job_id)
        return jsonify({'job': job.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators',
                  'start_date', 'end_date', 'is_finished'))})

    def delete(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.get(Jobs, job_id)
        session.delete(job)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, job_id):
        abort_if_job_not_found(job_id)
        session = db_session.create_session()
        job = session.get(Jobs, job_id)

        args = put_parser.parse_args()

        if args['team_leader'] is not None:
            job.team_leader = args['team_leader']
        if args['job'] is not None:
            job.job = args['job']
        if args['work_size'] is not None:
            job.work_size = args['work_size']
        if args['collaborators'] is not None:
            job.collaborators = args['collaborators']
        if args['start_date'] is not None:
            try:
                job.start_date = datetime.strptime(args['start_date'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                abort(400, message='Invalid date format. Use YYYY-MM-DD HH:MM:SS')
        if args['end_date'] is not None:
            try:
                job.end_date = datetime.strptime(args['end_date'], '%Y-%m-%d %H:%M:%S')
            except ValueError:
                abort(400, message='Invalid date format. Use YYYY-MM-DD HH:MM:SS')
        if args['is_finished'] is not None:
            job.is_finished = args['is_finished']

        session.commit()
        return jsonify({'success': 'OK'})


parser = reqparse.RequestParser()
parser.add_argument('team_leader', required=True, type=int)
parser.add_argument('job', required=True)
parser.add_argument('work_size', required=True, type=int)
parser.add_argument('collaborators', required=True)
parser.add_argument('start_date', required=True)
parser.add_argument('end_date', required=True)
parser.add_argument('is_finished', required=True, type=bool)

put_parser = reqparse.RequestParser()
put_parser.add_argument('team_leader', type=int)
put_parser.add_argument('job')
put_parser.add_argument('work_size', type=int)
put_parser.add_argument('collaborators')
put_parser.add_argument('start_date')
put_parser.add_argument('end_date')
put_parser.add_argument('is_finished', type=bool)


class JobsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        jobs = session.query(Jobs).all()
        return jsonify({'jobs': [item.to_dict(
            only=('team_leader', 'job', 'work_size', 'collaborators', 'is_finished')) for item in jobs]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        jobs = Jobs(
            team_leader=args['team_leader'],
            job=args['job'],
            work_size=args['work_size'],
            collaborators=args['collaborators'],
            is_finished=args['is_finished'],
            start_date=args['start_date'],
            end_date=args['end_date']
        )
        session.add(jobs)
        session.commit()
        return jsonify({'id': jobs.id})
