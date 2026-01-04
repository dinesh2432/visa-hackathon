// Import the module

export const fileMetaDataExtraction = (req, res) => {
    try {
        console.log(req.files);
        if (!req.files || Object.keys(req.files).length === 0) {
            console.log("No files were uploaded.");
            return res.status(400).json({ message: 'No files were uploaded.' });
        }

        // Access the file (assuming key is 'file')
        const uploadedFile = req.files.file;

        return res.status(200).json({
            message: 'File uploaded successfully',
            file: {
                name: uploadedFile.name,
                size: uploadedFile.size,
                mimetype: uploadedFile.mimetype,
                md5: uploadedFile.md5
            }
        });

    } catch (err) {
        return res.status(500).json({
            message: err.message
        });
    }
};