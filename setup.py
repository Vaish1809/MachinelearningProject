##Create a ml project as a package and then can also be deployed
from setuptools import find_packages,setup #finds all packages req  

def get_requirements(file_path: str)-> list[str]:
    '''
    This function will return a list of requirements
    '''
    requirements = []
    with open(file_path) as file_obj:
        requirements = file_obj.readlines()
        requirements = [req.replace('\n', '') for req in requirements]
    
    #if -e . is present then remove it
    if '-e .' in requirements:
        requirements.remove('-e .')
    
    return requirements
setup(

    name='mlproject',
    version='0.0.1',
    author='Vaishnavi',
    author_email= 'Vaishnavipadiya@gmail.com',
    packages=find_packages(), #finds all packages in the directory
    install_requires=get_requirements('requirements.txt')#dependencies


)