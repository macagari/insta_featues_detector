# parametri : username
# password
# images_numbers:
# timeout=5000
# profile
# images_directory = /data

from model.components import Arg, Component, save_extensions, Input, Output, AsyncSelect, Dynamic

download = Input(id='input',
                 label='Download',
                 service='download_images',
                 to='output_download_images')

download_ = Output(id='output_download_images',
                   label='Download')

username = Arg(name="username",
               type="text",
               label="Username",
               helper="Instagram Username to log in ",
               value="macagari"
               )

password = Arg(name="password",
               type="password",
               label="Password",
               value="Garcia1067")

images_numbers = Arg(name="images_numbers",
                     type="number",
                     label="Images Number",
                     helper="Total images to download",
                     value=2)

timeout = Arg(name="timeout",
              type="number",
              label="Timeout Value",
              helper="Set a higher timeout value if your internet connectio is slow",
              value=5000)

profile_name = Arg(name="profile",
                   type="text",
                   label="Profile Name",
                   helper="Specify an Instragram public profile where to download the images",
                   value="lancomeofficial")

images_directory = Arg(name="images_directory",
                       type="directories",
                       label="Images Directory",
                       helper="Select a directory where to save the images",
                       value="images_instagram")

images_instagram = Component(name="Images Instagram",
                             args=[username, password, profile_name, images_numbers, images_directory, timeout],
                             inputs=[download],
                             outputs=[download_],
                             configured=False,
                             trigger=True,
                             icon="RiPolaroid2Line")


save_extensions([images_instagram])
