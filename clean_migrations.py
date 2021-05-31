import fnmatch
import os


def list_migrations_in_apps(target_path):
    base_path = os.path.join(target_path, 'apps')
    result = dict()
    migrations_path = 'migrations'
    migration_file_id = 1
    for app_full_path, sub_dirs, files in os.walk(base_path):
        if migrations_path in sub_dirs:
            mig_dir = os.path.join(app_full_path, migrations_path)
            files_list = os.listdir(mig_dir)
            for entry in files_list:
                if not fnmatch.fnmatch(entry, '__init__.py'):
                    migration_file = os.path.join(mig_dir, entry)
                    result[migration_file_id] = migration_file
                    migration_file_id = migration_file_id + 1
    return result


def list_all_file_by_id(migrations_files, base_path):
    print('ID', '\t', 'Migrations File In App')
    print('-' * 50)
    for mk in migrations_files.keys():
        print(mk, '\t', migrations_files[mk].replace(base_path, ''))
    print('-' * 50)


def remove_file(file_path, base_path):
    if os.path.isfile(file_path):
        os.remove(file_path)
        print("Success: %s has been clean" % file_path.replace(base_path, ''))
    else:
        print("Error: %s not found" % file_path.replace(base_path, ''))


def main():
    try:
        root_path = os.path.dirname(os.path.realpath(__file__))
        migrations_files = list_migrations_in_apps(root_path)
        if not migrations_files:
            raise Exception('Not migrations need to be clean')
        list_all_file_by_id(migrations_files, root_path)
        target_mk = int(input('Please select delete migration file ID, if 0 will clear all:'))

        if target_mk is 0:
            for mk in migrations_files.keys():
                remove_file(migrations_files[mk], root_path)
        else:
            remove_file(migrations_files[target_mk], root_path)
    except Exception as e:
        print("Warning: {}".format(e))
    except KeyboardInterrupt:
        # User interrupt the program with ctrl+c
        print('')
        exit('User exit...')


if __name__ == '__main__':
    main()
