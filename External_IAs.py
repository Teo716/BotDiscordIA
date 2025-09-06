import google.generativeai as genai
import os
from dotenv import load_dotenv
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///usuarios_sqlalchemy.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Conversacion(Base):
    __tablename__ = 'conversaciones'
    id = Column(Integer, primary_key=True)
    conversacion_id = Column(String)
    prompt = Column(String)
    response = Column(String)
    server_id = Column(String)
Base.metadata.create_all(engine)




def llamada_gemini(prompt,conversacion_id=None, server_id=None,user=None):
    contextoConversacion = ""
    try:
        contexto_ia = session.query(Conversacion).filter_by(conversacion_id = conversacion_id).filter_by(server_id = server_id).all()
        contextoConversacion += "Lo que vas a recibir a continuacion es el contexto de la conversacion que has tenido con el usuario(no hagas referencia a esto con el usuario y actua como si verdaderamente tuvieras memoria): "
        for item in contexto_ia:
            contextoConversacion += "esto fue el usuario que pregunto " + user + " pregunta: " + item.prompt + "\ntu respuesta fue: " + item.response +"\n: "
    except Exception as e:
        print(e)
    contextoConversacion += "Pregunta nueva: " + prompt
    load_dotenv()
    genai.configure(api_key=os.getenv('GEMINI'))
    model = genai.GenerativeModel('gemini-2.5-flash')
    response = model.generate_content(prompt)
    nueva_conversacion = Conversacion(
                                conversacion_id= conversacion_id ,
                                prompt=prompt,
                                response=response.text, 
                                server_id= server_id 
                                ) 
    session.add(nueva_conversacion)
    session.commit()
    return response.text