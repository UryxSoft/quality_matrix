from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# Modelo de procesos
class Proceso(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    indicadores = db.relationship('Indicador', backref='proceso', lazy=True)

# Modelo de indicadores
class Indicador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    descripcion = db.Column(db.String(200))
    unidad = db.Column(db.String(50))
    proceso_id = db.Column(db.Integer, db.ForeignKey('proceso.id'), nullable=False)
    metas = db.relationship('Meta', backref='indicador', lazy=True)
    valores = db.relationship('Valor', backref='indicador', lazy=True)

# Modelo de metas
class Meta(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    indicador_id = db.Column(db.Integer, db.ForeignKey('indicador.id'), nullable=False)

# Modelo de valores reales
class Valor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Float, nullable=False)
    anio = db.Column(db.Integer, nullable=False)
    mes = db.Column(db.Integer, nullable=False)
    calificacion = db.Column(db.Float)
    indicador_id = db.Column(db.Integer, db.ForeignKey('indicador.id'), nullable=False)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)