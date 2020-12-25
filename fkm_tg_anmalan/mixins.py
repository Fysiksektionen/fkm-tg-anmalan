from fkm_tg_anmalan.models import Site


class SiteMixin:
    site_name = None
    site_texts = []
    site_images = []
    site_files = []
    site_paragraph_lists = []

    def get_site_context(self):
        if self.site_name:
            site_context = {}
            site = Site.get_populated_site(self.site_name, self.site_texts, self.site_images, self.site_files, self.site_paragraph_lists, True)

            texts_list = site.texts.values_list('key', 'text')
            images_list = site.images.values_list('key', 'image')
            files_list = site.files.values_list('key', 'file')
            paragraphs_lists = [(para_list, para_list.paragraphs.all()) for para_list in site.paragraph_lists.all()]
            site_context.update({
                'texts': {key_text_pair[0]: key_text_pair[1] for key_text_pair in texts_list},
                'images': {key_image_pair[0]: key_image_pair[1] for key_image_pair in images_list},
                'files': {key_file_pair[0]: key_file_pair[1] for key_file_pair in files_list},
                'lists': {
                    key_list_pair[0].key: [
                        {
                            'order_num': para.order_num,
                            'title': para.title,
                            'text': para.text,
                            'image': para.image
                        } for para in key_list_pair[1].order_by(
                            ('' if key_list_pair[0].ascending_order else '-') + 'order_num'
                        )
                    ] for key_list_pair in paragraphs_lists
                }
            })

            return site_context
        else:
            return {}

    def get_context_data(self, **kwargs):
        super_context = super().get_context_data(**kwargs)
        super_context.update({
            'site': self.get_site_context()
        })
        return super_context
