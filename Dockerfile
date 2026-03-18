#Importing Python package
FROM python:3.13-slim

# #Creating a non-root user and the home directory
RUN useradd --create-home appuser

#Setting the working directory and installing necessary package
WORKDIR /home/appuser/main_app

RUN apt-get update
RUN apt-get install -y ffmpeg

#Copy the necessary project file to the docker image
COPY requirements.txt /home/appuser/main_app/
COPY encrypted/pyarmor_runtime_000000/ /home/appuser/main_app/pyarmor_runtime_000000
COPY encrypted/app.py /home/appuser/main_app/
COPY encrypted/app/ /home/appuser/main_app/app/
COPY nginx/nginx.conf /etc/nginx/
COPY __pycache__/ /home/appuser/main_app/__pycache__/

#installing the Application dependencies
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn 

#Port that will be used
EXPOSE 5000/tcp

#Create new directory to save logs and temporary files
RUN mkdir /usr/tmp && chown -R appuser:appuser /usr/tmp
RUN mkdir -p /home/appuser/main_app/app/templates/logs

#Set the ownership of the folder
RUN chown -R appuser:appuser /home/appuser
RUN chown -R appuser:appuser /tmp
RUN chown -R appuser:appuser /var/tmp
RUN chown -R appuser:appuser /etc/nginx


#change the user from root to non-root user
USER appuser

#Running the flask command using gunicorn and saving the detailed logs
CMD ["gunicorn", "-b", "0.0.0.0:5000", "-w", "1", "-t" , "4", "--preload" ,  "app:app",  "--log-level", "debug", "--access-logfile", "/home/appuser/main_app/app/templates/logs/access.log", "--error-logfile", "/home/appuser/main_app/app/templates/logs/error.log"]
