# -*- coding: utf-8 -*-


from distutils.core import setup
setup(
  name = 'liveupstoxoc',         
  packages = ['liveupstoxoc'],   
  version = '0.1',      
  license='MIT',        
  description = 'To scrape live optionschain data from upstox for free (without api)',   
  author = 'Niraj Munot',                   
  author_email = 'nirajmunot28@gmail.com',      
  url = 'https://github.com/MaticAlgos',   
  download_url = 'https://github.com/MaticAlgos/liveupstoxoc/archive/refs/tags/0.1.2.tar.gz',    
  keywords = ['upstox', 'optionschain', 'liveoptionschain', "NSE", "openinterest"],   
  install_requires=[            
          'selenium',
          'beautifulsoup4',
          "pandas"
          
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
