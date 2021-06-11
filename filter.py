def remove_single_object(image, r, index):
    # i is the id of one particular mask
    filtered = image.copy()
    cropped = image.copy()
    mask = r["masks"][:, :, index]
    for j in range(cropped.shape[2]):
        cropped[:, :, j] = image[:, :, j] * mask[:, :]
        filtered[:, :, j] = image[:, :, j] - cropped[:, :, j]
    return [filtered, cropped]


def remove_multi_object(image, r):
    filtered = image.copy()
    cropped = image.copy()
    mask = r["masks"][:, :, 0]
    for i in range(1, r["masks"].shape[2]):
        mask += r["masks"][:, :, i]
    for j in range(filtered.shape[2]):
        filtered[:, :, j] = image[:, :, j] - image[:, :, j] * mask
    return [filtered, cropped]
