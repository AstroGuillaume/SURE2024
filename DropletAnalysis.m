
wd = "C:/Users/guill/Documents/SURE 2024/";
output_dir = strcat(wd, "Modified Droplet Pictures/");


% run through the desired pictures in the dataset (1 to 9)
for i = 1:9
    % Correct the format string for the input path
    path = sprintf("Droplet Pictures/june 21 test 5 (10 uL) piston and compressor turned at 10mS delay (25.3 PSI)_C001H001S000100055%d.png", i);
    input_path = strcat(wd, path);

    % Read and write image
    file = strcat(output_dir, sprintf("image%d.tif", i));
    image = imread(input_path);
    imwrite(image, file, 'tif');
end


% Define the output path
input_path = strcat(output_dir, "image*.tif");
output_path = strcat(output_dir, "output.tif");

% Use the correct output path in the BackgroundImage function call
BackgroundImage(input_path, output_path);

% Define the input parameters
inputnames = 'image*.tif';     % Pattern for image file names
threshold = 4;                % Intensity threshold
max_disp = 200;                % Maximum displacement
bground_name = 'output.tif';   % Background image file (optional)


% Call the PredictiveTracker function
[vtracks, ntracks, meanlength, rmslength] = PredictiveTracker(fullfile(output_dir, inputnames), threshold, max_disp, bground_name);

% Display the results
disp(['Number of tracks: ', num2str(ntracks)]);
%% 
disp(['Mean track length: ', num2str(meanlength)]);
disp(['RMS track length: ', num2str(rmslength)]);


for i = 1:9
    input = sprintf("Modified Droplet Pictures\\input%d.tif", i);

    % Read the original image
    image = imread(fullfile(wd, path));

    % Assuming vtracks contains the required fields
    % Loop through each track
    for j = 1:length(vtracks.len)
        diameter = vtracks.len(j);  % Diameter of the circle
        x = vtracks.X(j);           % X position of the circle center
        y = vtracks.Y(j);           % Y position of the circle center

        % Draw the circle on the image
        image = insertShape(image, 'FilledCircle', [x y diameter/2], 'Color', 'red');
        imshow(image);
    end
end